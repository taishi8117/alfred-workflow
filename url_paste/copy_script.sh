query=$1

echo $query | sed 's/} {/}{/g' | sed 's/ \\deftab720/\\deftab720/g' | pbcopy
