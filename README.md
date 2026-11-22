# Check

node scripts/publish/publish.mjs --channels          # ověří Buffer klíč, vypíše 3 kanály
node scripts/publish/publish.mjs --dry 003

# Publish
node scripts/publish/publish.mjs 003


# TODO

- Pridat at se kazde video generuje do sve slozky, at ji muzu kdykoliv smazat. At se tam davaji jen ty veci, tkere jsou specificke pouze pro to dane video. Pokud se prida neco, co ma realnou sanci se jeste nekdy pouzit, tak at se to prida normlane do archivu tohoto projektu. To co tam nemusi byt - proste specificke veci pro dane video, tak at to jde do te slozky at to pak muzu smazat. Chci at muzu generovat vice videi najednou kdyztak. At se to navzajem nijak neovlivni