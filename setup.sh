# python version 3.10.7

rm -R ./env
python -m venv env

./env/Scripts/python.exe -m pip install --upgrade pip

./env/Scripts/pip.exe install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121 --default-timeout=50000
./env/Scripts/pip.exe install transformers
./env/Scripts/pip.exe install accelerate

$env:CMAKE_ARGS = "-DLLAMA_CUBLAS=on"
$env:FORCE_CMAKE = 1
./env/Scripts/pip.exe install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

./env/Scripts/pip.exe install flask

# for git-bash
read -p "End to enter."