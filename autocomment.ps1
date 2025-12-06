#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Auto Commenter - PowerShell Wrapper
    Run from anywhere with: autocomment.ps1 <file> [output_file]

.DESCRIPTION
    This script runs the Auto Commenter using Pipenv, allowing you to use
    the tool from any directory.

.PARAMETER FilePath
    The code file to comment, or directory to process

.PARAMETER OutputFile
    Optional output file path

.EXAMPLE
    .\autocomment.ps1 script.py
    .\autocomment.ps1 script.py output.py
    .\autocomment.ps1 ./src/
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FilePath,
    
    [Parameter(Mandatory=$false, Position=1)]
    [string]$OutputFile
)

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if pipenv is available
try {
    $pipenvVersion = pipenv --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Pipenv not found"
    }
} catch {
    Write-Host "Error: Pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Change to the script directory and run
Push-Location $scriptDir
try {
    if ($OutputFile) {
        & pipenv run python auto_commenter.py $FilePath $OutputFile
    } else {
        & pipenv run python auto_commenter.py $FilePath
    }
} finally {
    Pop-Location
}
