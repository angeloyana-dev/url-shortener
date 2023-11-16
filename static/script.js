const output = document.querySelector("input[id=output]")
function copyOutput() {
    output.select()
    document.execCommand("copy")
}