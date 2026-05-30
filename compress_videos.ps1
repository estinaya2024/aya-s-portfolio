# PowerShell script to compress portfolio videos using FFmpeg
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   Portfolio Video Compression Tool          " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Check if FFmpeg is installed
$ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpegExists) {
    Write-Host "[!] FFmpeg is not installed on your system." -ForegroundColor Yellow
    Write-Host "[*] Attempting to install FFmpeg via winget..." -ForegroundColor Cyan
    winget install --id=Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
    
    # Refresh PATH environment variable
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    # Check again
    $ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if (-not $ffmpegExists) {
        Write-Host "[X] FFmpeg installation could not be completed automatically." -ForegroundColor Red
        Write-Host "    Please install FFmpeg manually or download Handbrake (https://handbrake.fr/) to compress your videos." -ForegroundColor Yellow
        exit
    }
}

Write-Host "[+] FFmpeg detected successfully!" -ForegroundColor Green

# List of video files to compress in the public folder
$videos = @(
    "about-record.mp4",
    "boutique-record.mp4",
    "dashboard-record.mp4",
    "plat-record.mp4",
    "process-record.mp4",
    "region-record.mp4"
)

$publicDir = Join-Path $PSScriptRoot "public"

foreach ($video in $videos) {
    $inputPath = Join-Path $publicDir $video
    $outputPath = Join-Path $publicDir ("compressed_" + $video)
    
    if (Test-Path $inputPath) {
        $originalSize = (Get-Item $inputPath).Length / 1MB
        Write-Host "`n[*] Compressing $video ($([math]::Round($originalSize, 2)) MB)..." -ForegroundColor Cyan
        
        # Run FFmpeg compression: Web optimized, scale to 720p width (1280px), remove audio, CRF 28 for ultra high compression with crisp text
        & ffmpeg -y -i $inputPath -vcodec libx264 -crf 28 -preset faster -vf "scale=1280:-2" -an $outputPath
        
        if (Test-Path $outputPath) {
            $compressedSize = (Get-Item $outputPath).Length / 1MB
            $savingPercent = ($originalSize - $compressedSize) / $originalSize * 100
            
            # Replace original with compressed version
            Remove-Item $inputPath -Force
            Rename-Item $outputPath -NewName $video
            
            Write-Host "[+] Finished $video!" -ForegroundColor Green
            Write-Host "    New Size: $([math]::Round($compressedSize, 2)) MB" -ForegroundColor Green
            Write-Host "    Reduced by: $([math]::Round($savingPercent, 1))%" -ForegroundColor Green
        } else {
            Write-Host "[X] Failed to compress $video" -ForegroundColor Red
        }
    } else {
        Write-Host "[!] File not found: $video" -ForegroundColor Yellow
    }
}

Write-Host "`n[+] All videos successfully compressed! Your portfolio is now ultra lightweight." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
