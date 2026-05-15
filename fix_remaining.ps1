$root = "F:\TianshangKnowledgeBase"
$allMd = [System.IO.Directory]::GetFiles($root, "*.md", [System.IO.SearchOption]::AllDirectories) | Where-Object { $_ -notmatch '\\\\node_modules\\\\' }

Write-Host "Total .md files: $($allMd.Count)"

$countAdded = 0
$countSkipped = 0
$encoding = [System.Text.UTF8Encoding]::new($false)  # UTF-8 no BOM

function Get-SiblingLinks($dir, $currentFile) {
    $siblings = [System.IO.Directory]::GetFiles($dir, "*.md") | Where-Object { $_ -ne $currentFile }
    $links = @()
    foreach ($sib in $siblings) {
        $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($sib)
        $sibName = [System.IO.Path]::GetFileName($sib)
        if ($sibName -eq "INDEX.md") {
            $dirName = [System.IO.Path]::GetFileName($dir.TrimEnd('\'))
            $links += "- [[$nameWithoutExt|$dirName 索引]]"
        } else {
            $links += "- [[$nameWithoutExt]]"
        }
    }
    return $links
}

function Get-AncestorIndexLinks($dir, $root) {
    $links = @()
    $d = [System.IO.Directory]::GetParent($dir)
    $relDepth = 1
    while ($d -and $d.FullName.Length -ge $root.Length) {
        $indexFile = [System.IO.Path]::Combine($d.FullName, "INDEX.md")
        if ([System.IO.File]::Exists($indexFile)) {
            $name = [System.IO.Path]::GetFileName($d.FullName.TrimEnd('\'))
            $prefix = "..\" * $relDepth
            $prefix = $prefix.TrimEnd('\')
            $links += "- [[$prefix/INDEX|$name 索引]]"
        }
        $d = $d.Parent
        $relDepth++
    }
    return $links
}

foreach ($filePath in $allMd) {
    $content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    $hasSection = $content.Contains("## 相关条目")
    $hasLinks = $content.Contains("[[")

    if (-not $hasLinks) {
        $dir = [System.IO.Path]::GetDirectoryName($filePath)
        $siblingLinks = Get-SiblingLinks $dir $filePath
        $ancestorLinks = Get-AncestorIndexLinks $dir $root
        $addLinks = @()
        $addLinks += "## 相关条目"
        $addLinks += ""
        foreach ($link in $siblingLinks) { $addLinks += $link }
        foreach ($link in $ancestorLinks) { $addLinks += $link }
        if ($addLinks.Count -gt 2) {
            $newContent = $content.TrimEnd() + "`r`n`r`n" + ($addLinks -join "`r`n") + "`r`n"
            [System.IO.File]::WriteAllText($filePath, $newContent, $encoding)
            Write-Host "NO_LINKS_FIXED: $filePath"
            $countAdded++
        }
        continue
    }

    if (-not $hasSection) {
        $dir = [System.IO.Path]::GetDirectoryName($filePath)
        $siblingLinks = Get-SiblingLinks $dir $filePath
        $ancestorLinks = Get-AncestorIndexLinks $dir $root
        $newLinks = @()
        $newLinks += ""
        $newLinks += "## 相关条目"
        foreach ($link in $siblingLinks) { $newLinks += $link }
        foreach ($link in $ancestorLinks) { $newLinks += $link }
        $newContent = $content.TrimEnd() + "`r`n" + ($newLinks -join "`r`n") + "`r`n"
        [System.IO.File]::WriteAllText($filePath, $newContent, $encoding)
        Write-Host "ADDED: $filePath"
        $countAdded++
    } else {
        $countSkipped++
    }
}

Write-Host "`n=== Summary ==="
Write-Host "Added/fixed sections: $countAdded"
Write-Host "Skipped (already had): $countSkipped"
