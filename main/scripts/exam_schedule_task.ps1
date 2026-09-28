<#
시험정보 탭의 연간일정계획(analytics.ExamSchedule)을 갱신하는 스크립트.
파일 하나로 "실행 대상"과 "스케줄 등록"을 겸한다.

사용법
  인자 없이 실행         -> 실제 갱신 작업을 1회 수행 (Windows 작업 스케줄러가 이 모드로 호출)
  -Register 옵션으로 실행 -> Windows 작업 스케줄러에 $IntervalHours 주기로 이 스크립트를 등록/갱신

  powershell -ExecutionPolicy Bypass -File .\exam_schedule_task.ps1 -Register

실행 주기를 바꾸려면 $IntervalHours 값만 수정하고 -Register로 다시 실행하면 된다.
#>
param(
    [switch]$Register
)

$TaskName = "SportsCareerCompass_RefreshExamSchedule"
$IntervalHours = 12
$StartTime = "00:00"

$ScriptPath = $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path $PSScriptRoot -Parent            # ...\main
$RepoRoot = Split-Path $ProjectRoot -Parent                 # ...\Noanswer3Brothers
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$LogPath = Join-Path $ProjectRoot "logs\refresh_exam_schedule.log"

if ($Register) {
    $action = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
    $trigger = New-ScheduledTaskTrigger -Once -At $StartTime `
        -RepetitionInterval (New-TimeSpan -Hours $IntervalHours) `
        -RepetitionDuration (New-TimeSpan -Days 3650)

    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Force | Out-Null
    Write-Host "Registered: $TaskName runs every $IntervalHours hour(s), starting at $StartTime"
}
else {
    New-Item -ItemType Directory -Force -Path (Split-Path $LogPath) | Out-Null
    Set-Location $ProjectRoot
    & $VenvPython manage.py refresh_exam_schedule *>> $LogPath
}
