nastavujeme prokazování identity (login) skrz SSH (asymetrická kryptografie)

## Vygenerování páru kličů

- z příkazové řádky pomocí `ssh-keygen` vygenerujge **privátní** a **veřejný** klíč
- ponechte defaultní pojmenování (`id_ed25519`)
- heslo si zvolte jednoduše zapamatovatelné, toto heslo budete potřebovat vždy při použití privátního kliče
- soubory:
  - vygenerují se do `$HOME/.ssh` složky
  - privátní klíč je bez přípony
  - veřejný klíč má příponu `pub`

## Nastavení na GitHub

- jděte do svého profilu, nastavení:
<img width="326" height="662" alt="image" src="https://github.com/user-attachments/assets/416bb29d-6866-4df0-b40d-65eedd05f4c0" />

- pak zvolte `SSH and GPG keys`:
<img width="1317" height="571" alt="image" src="https://github.com/user-attachments/assets/8c9a9523-445d-4c6d-89c2-5fb960baf391" />

- kliněte na `New SSH key`:
<img width="978" height="509" alt="image" src="https://github.com/user-attachments/assets/f891fc45-b753-4dc4-9b7d-b956c4e395e0" />

- do `Key` vložte **obsah** souboru `~/.ssh/id_ed25519.pub` (obsah vypište třeba příkazem `cat`)
- pak kliněte na `Add SSH key` tlačítko
- tím jste dali githubu vědět svůj veřený klíč

## První použití

- za předpokladu, že máte vytvořené své první soukromé repo můžete zkus klon tohoto soukromého repozitáře
```
git clone git@github.com:pavelkryl/moje-prvni-repo.git
```
- odkaz najdete na stránce repozitáře (tlačítko ssh - odkaz musí začínat `git@...`):
<img width="1251" height="444" alt="image" src="https://github.com/user-attachments/assets/fdc861d4-8927-4d08-8e17-b007848211af" />

- po od-Enterování příkazu `git clone` se bude chtít prokázat vaše identita pomocí použití privátního klíče
- vyskočí na vás dialogové okno operačního systému pro zadání hesla k privátnímu klíči
- musíte napsat heslo a můžete zaškrtnout volbu, že se vás příště nemá ptát, že si má heslo zapamatovat (doporučuji zaškrtnout)

