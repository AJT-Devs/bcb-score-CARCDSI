$ErrorActionPreference = 'Stop'
# Python portátil no projeto; nenhuma instalação no sistema operacional.
New-Item -ItemType Directory -Force .tools | Out-Null
if (-not (Test-Path .tools/uv/uv.exe)) {
    Invoke-WebRequest https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip -OutFile .tools/uv.zip
    Expand-Archive .tools/uv.zip -DestinationPath .tools/uv -Force
}
& .tools/uv/uv.exe python install 3.14.0 --install-dir .tools/python --no-bin
if ($LASTEXITCODE -ne 0) { throw 'Falha no download de Python' }
& .tools/uv/uv.exe venv --python .tools/python/cpython-3.14.0-windows-x86_64-none/python.exe .venv
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar venv' }
& .tools/uv/uv.exe pip install --python .venv/Scripts/python.exe -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependências' }
