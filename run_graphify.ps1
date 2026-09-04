<#
.SYNOPSIS
    Script para preparar o ambiente local e executar o Graphify.
#>

Write-Host "🚀 A iniciar configuração do ambiente para o Graphify..." -ForegroundColor Cyan

# 1. Carregar o NODE2 do ficheiro .env
$EnvPath = Join-Path $PSScriptRoot ".env"
$Node2 = "localhost"
if (Test-Path $EnvPath) {
    $NodeLine = Get-Content $EnvPath | Select-String "^NODE2="
    if ($NodeLine) {
        $Node2 = ($NodeLine -split "=")[1].Trim().Trim('"').Trim("'")
    }
} else {
    Write-Host "⚠️ Ficheiro .env não encontrado. A usar fallback: $Node2" -ForegroundColor Yellow
}

# Definir as variáveis de ambiente necessárias para o backend Ollama (LM Studio)
$env:OLLAMA_BASE_URL="http://${Node2}:1234/v1"
$env:OLLAMA_MODEL="qwen/qwen3.5-9b"
$env:OLLAMA_API_KEY="lm-studio"
#$env:GRAPHIFY_OLLAMA_NUM_CTX="65536"  # Aumenta a janela de contexto para 64k tokens
#$env:GRAPHIFY_MAX_OUTPUT_TOKENS="8192" # Permite até 8192 tokens de resposta para extrações densas (máximo suportado por local backends)

$MaxWorkers = [math]::Min(61, [math]::Max(2, [int]($env:NUMBER_OF_PROCESSORS * 0.75)))

Write-Host "✅ Variáveis de ambiente configuradas:" -ForegroundColor Green
Write-Host "   OLLAMA_BASE_URL     = $env:OLLAMA_BASE_URL"
Write-Host "   OLLAMA_MODEL        = $env:OLLAMA_MODEL"
#Write-Host "   NUM_CTX             = $env:GRAPHIFY_OLLAMA_NUM_CTX"
#Write-Host "   MAX_OUTPUT_TOKENS   = $env:GRAPHIFY_MAX_OUTPUT_TOKENS"
Write-Host "   AST Workers (Host)  = $MaxWorkers"

# 2. Executar a extração semântica com o backend Ollama (compatível com LM Studio) otimizada para APU Strix Halo 64GB
#Write-Host "🧠 A executar 'graphify extract . --backend ollama --token-budget 49152 --max-workers $MaxWorkers --max-concurrency 2 --api-timeout 600'..." -ForegroundColor Cyan
#.venv\Scripts\python.exe -m graphify extract . --backend ollama --token-budget 49152 --max-workers $MaxWorkers --max-concurrency 2 --api-timeout 600

#Write-Host "🧠 A executar 'graphify extract . --backend ollama --max-workers $MaxWorkers --max-concurrency 2 --api-timeout 600'..." -ForegroundColor Cyan
#.venv\Scripts\python.exe -m graphify extract . --backend ollama --max-workers $MaxWorkers --max-concurrency 2 --api-timeout 600

Write-Host "🧠 A executar 'graphify . --backend ollama --max-workers $MaxWorkers --max-concurrency 1 --token-budget 8192 --api-timeout 1600'..." -ForegroundColor Cyan
.venv\Scripts\python.exe -m graphify . --backend ollama --max-workers $MaxWorkers --max-concurrency 1 --token-budget 8192 --api-timeout 1600

.venv\Scripts\python.exe -m graphify cluster-only .

Write-Host "✨ Processo concluído!" -ForegroundColor Green