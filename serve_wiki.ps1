# serve_wiki.ps1
# Script to serve the local EasyIot documentation wiki using MkDocs,
# while verifying that the port is not used by other Antigravity-linked projects.

$ErrorActionPreference = "Stop"

# Current project directory
$CurrentDir = (Get-Item .).FullName
$CurrentDirNorm = $CurrentDir.ToLower().Replace("/", "\")

# Load Antigravity projects
$ProjectsJsonPath = "C:\Users\bruno\.gemini\projects.json"
$Projects = @{}
if (Test-Path $ProjectsJsonPath) {
    try {
        $Json = Get-Content $ProjectsJsonPath -Raw | ConvertFrom-Json
        if ($Json.projects) {
            $Projects = $Json.projects
        }
    } catch {
        Write-Warning "Could not parse Antigravity projects.json: $_"
    }
}

# Function to identify if a PID (or its parent processes) belongs to an Antigravity project
function Get-ProjectForProcess {
    param(
        [int]$ProcessId
    )
    if (-not $ProcessId) { return $null }

    $currPid = $ProcessId
    # Trace up to 3 parent process levels to resolve python shims/wrappers
    for ($depth = 0; $depth -lt 3; $depth++) {
        if (-not $currPid) { break }
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $currPid" -ErrorAction SilentlyContinue
        if (-not $proc) { break }

        $cmdLine = $proc.CommandLine
        $exePath = $proc.ExecutablePath
        $cmdLineNorm = if ($cmdLine) { $cmdLine.ToLower().Replace("/", "\") } else { "" }
        $exePathNorm = if ($exePath) { $exePath.ToLower().Replace("/", "\") } else { "" }

        # Check if the process is from the current project
        if ($cmdLineNorm.Contains($CurrentDirNorm) -or $exePathNorm.Contains($CurrentDirNorm)) {
            return @{ Path = $CurrentDir; Name = "EasyIot (Current)"; IsCurrent = $true; ProcessName = $proc.Name }
        }

        # Check other Antigravity projects
        $matches = @()
        foreach ($prop in $Projects.PSObject.Properties) {
            $projPath = $prop.Name
            $projName = $prop.Value
            $projPathNorm = $projPath.ToLower().Replace("/", "\")

            # Don't match the current project folder again if listed
            if ($projPathNorm -eq $CurrentDirNorm) { continue }

            if ($cmdLineNorm.Contains($projPathNorm) -or $exePathNorm.Contains($projPathNorm)) {
                $matches += @{ Path = $projPath; Name = $projName; Length = $projPath.Length; IsCurrent = $false; ProcessName = $proc.Name }
            }
        }

        if ($matches.Count -gt 0) {
            return $matches | Sort-Object Length -Descending | Select-Object -First 1
        }

        # Move to parent process
        $currPid = $proc.ParentProcessId
    }

    # If no match is found in the chain, return the original process name
    $origProc = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
    $name = if ($origProc) { $origProc.Name } else { "Unknown" }
    return @{ Path = $null; Name = $null; IsCurrent = $false; ProcessName = $name }
}

# Start searching for a port
$Port = 8000
$PortFound = $false

Write-Host "Scanning for an available port starting at $Port..." -ForegroundColor Cyan

while (-not $PortFound) {
    # Check if anything is listening on $Port
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        # Port is in use
        $OwningPid = $conn[0].OwningProcess
        $ProjInfo = Get-ProjectForProcess -ProcessId $OwningPid

        if ($ProjInfo.IsCurrent) {
            Write-Host "Wiki is already running for the current project on port $Port (Process: $($ProjInfo.ProcessName), PID: $OwningPid)." -ForegroundColor Green
            Write-Host "Opening browser at http://127.0.0.1:$Port/ ..." -ForegroundColor Cyan
            Start-Process "http://127.0.0.1:$Port/"
            exit 0
        } elseif ($ProjInfo.Name) {
            Write-Host "[WARNING] Port $Port is in use by another Antigravity project: '$($ProjInfo.Name)' (Path: $($ProjInfo.Path), Process: $($ProjInfo.ProcessName), PID: $OwningPid)." -ForegroundColor Yellow
            Write-Host "Checking next port..." -ForegroundColor Gray
            $Port++
        } else {
            Write-Host "Port $Port is in use by a non-Antigravity process (Process: $($ProjInfo.ProcessName), PID: $OwningPid)." -ForegroundColor Gray
            Write-Host "Checking next port..." -ForegroundColor Gray
            $Port++
        }
    } else {
        $PortFound = $true
    }
}

Write-Host "Selected Port: $Port" -ForegroundColor Green
Write-Host "[START] Serving the documentation wiki locally on http://127.0.0.1:$Port ..." -ForegroundColor Cyan

# Start a background job to open the browser in 2 seconds
Start-Job -ScriptBlock {
    param($p)
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:$p/"
} -ArgumentList $Port | Out-Null

# Start mkdocs serve in foreground
.venv\Scripts\python.exe -m mkdocs serve -a "127.0.0.1:$Port"
