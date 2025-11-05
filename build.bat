@echo off
chcp 65001 > nul
echo Construindo Minha Moeda...

:: Verifica se as dependências estão instaladas
echo Verificando dependências...
python -c "import pandas, tkcalendar" 2>nul
if errorlevel 1 (
    echo Instalando dependências...
    pip install pandas tkcalendar
)

:: Verifica se o PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

:: Limpa builds anteriores
echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Executa o PyInstaller
echo Construindo executável...
pyinstaller minha_moeda.spec --clean

if exist dist\MinhaMoeda.exe (
    echo.
    echo ✅ Build concluído com sucesso!
    echo 📁 Executável: dist\MinhaMoeda.exe
    echo.
    echo 🚀 O aplicativo está pronto para uso!
    
    :: Testa o executável
    echo Testando o executável...
    timeout /t 3 > nul
    start dist\MinhaMoeda.exe
) else (
    echo.
    echo ❌ Erro no build!
    echo Verifique o arquivo warn-minha_moeda.txt para detalhes
    pause
)