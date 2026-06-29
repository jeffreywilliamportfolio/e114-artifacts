#!/usr/bin/env bash
# Runs ON the box, detached. Build capture binary -> wait for model -> run 3-arm capture -> tar.
exec > /workspace/drive_p1.log 2>&1
set -u
export PATH=$HOME/.local/bin:/usr/local/bin:/usr/local/cuda/bin:$PATH
echo "DRIVE_START $(date -u +%FT%TZ)"
python3 -m pip install -q --break-system-packages numpy 2>&1 | tail -1

# ---- build capture binary ----
cd /workspace/llama.cpp.new
git checkout 1772701f9 2>&1 | tail -1
mkdir -p examples/capture_activations
cp /workspace/probe3chunk/capture_activations.cpp examples/capture_activations/
cat > examples/capture_activations/CMakeLists.txt <<'EOF'
set(TARGET llama-capture-activations)
add_executable(${TARGET} capture_activations.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE common llama ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)
EOF
grep -q "add_subdirectory(capture_activations)" examples/CMakeLists.txt || echo "add_subdirectory(capture_activations)" >> examples/CMakeLists.txt
echo "=== cmake configure $(date -u +%T) ==="
cmake -S . -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release -DLLAMA_BUILD_EXAMPLES=ON -DCMAKE_CUDA_ARCHITECTURES=86 2>&1 | tail -4
echo "=== cmake build $(date -u +%T) ==="
cmake --build build --target llama-capture-activations -j"$(nproc)" 2>&1 | tail -8
cp build/bin/llama-capture-activations /workspace/probe3chunk/capture_activations 2>/dev/null && chmod +x /workspace/probe3chunk/capture_activations
if [ ! -x /workspace/probe3chunk/capture_activations ]; then echo "BUILD_FAILED"; exit 1; fi
echo "BINARY_SHA: $(sha256sum /workspace/probe3chunk/capture_activations)"

# ---- wait for model ----
MODEL=/workspace/models/hauhau/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf
echo "=== wait model $(date -u +%T) ==="
for i in $(seq 1 120); do
  if [ -f "$MODEL" ] && ! pgrep -f "hf download" >/dev/null; then echo "model ready iter $i"; break; fi
  sleep 10
done
if [ ! -f "$MODEL" ]; then echo "NO_MODEL"; exit 1; fi
ls -lh "$MODEL"

# ---- run capture ----
echo "=== ORCHESTRATOR $(date -u +%T) ==="
bash /workspace/probe3chunk/orchestrator_p1_causal.sh
echo "DRIVE_DONE $(date -u +%FT%TZ)"
