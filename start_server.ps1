# PowerShell script to start the Lost & Found server
Write-Host "Activating conda environment 'myenv'..." -ForegroundColor Green
conda activate myenv

Write-Host "Starting Lost & Found Backend Server..." -ForegroundColor Green
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Read-Host "Press Enter to exit"
