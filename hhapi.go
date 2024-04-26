package main

import (
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("cmd", "/k", "run.exe")
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Run()
}
