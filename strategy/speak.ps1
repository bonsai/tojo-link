Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = -1
$synth.Volume = 100

$text = Get-Content "C:\Users\dance\Documents\MEGA\tojo-link-board\docs\meeting-minutes-v1.txt" -Raw
$synth.Speak($text)
