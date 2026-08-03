<#
.SYNOPSIS
    Atualiza o React Dev Hub no Antigravity.

.DESCRIPTION
    Rode depois de um push para trazer a versao nova do plugin.
    Nao instala o plugin do zero -- para isso, veja o README.

    O Antigravity nao recarrega plugins em sessao aberta: reinicie o app
    ou reabra o workspace depois de atualizar.

.EXAMPLE
    powershell scripts/atualizar-plugin.ps1
    powershell scripts/atualizar-plugin.ps1 -LimparCache
#>
[CmdletBinding()]
param(
    [string]$Plugin = 'plugin-react-dev-toolkit',
    [switch]$LimparCache
)

$ErrorActionPreference = 'Continue'
$falhas = @()

function Titulo($t) { Write-Host ''; Write-Host "== $t" -ForegroundColor Cyan }
function Aviso($t)  { Write-Host "  $t" -ForegroundColor Yellow }
function Ok($t)     { Write-Host "  $t" -ForegroundColor Green }
function Existe($c) { $null -ne (Get-Command $c -ErrorAction SilentlyContinue) }

$pluginsDir = Join-Path $HOME '.gemini\config\plugins'

Titulo 'Antigravity'
if (Existe 'agy') {
    if ($LimparCache) {
        $pluginPath = Join-Path $pluginsDir $Plugin
        if (Test-Path $pluginPath) {
            Remove-Item -Recurse -Force $pluginPath
            Aviso "plugin removido: $pluginPath"
        }
        $cliPath = Join-Path $HOME '.gemini\antigravity-cli\plugins'
        if (Test-Path $cliPath) {
            $cliPlugin = Join-Path $cliPath $Plugin
            if (Test-Path $cliPlugin) {
                Remove-Item -Recurse -Force $cliPlugin
                Aviso "plugin CLI removido: $cliPlugin"
            }
        }
    }
    agy plugin update $Plugin
    if ($LASTEXITCODE -ne 0) { $falhas += 'agy plugin update' }
    Ok 'feito. Reinicie o Antigravity para carregar os arquivos novos.'
} else {
    Aviso "CLI 'agy' nao encontrada no PATH -- pulando."
    Aviso "Para atualizar manualmente: copie a pasta do plugin para $pluginsDir\$Plugin"
}

Write-Host ''
if ($falhas.Count -gt 0) {
    Write-Host "Falhou: $($falhas -join ', ')" -ForegroundColor Red
    exit 1
}
Ok 'Atualizacao concluida.'
