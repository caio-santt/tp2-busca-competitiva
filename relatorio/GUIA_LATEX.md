# Guia de Uso - LaTeX Workshop + Template AAAI

## 📋 Status Atual

✅ **Template AAAI**: Presente na pasta `relatorio/`
- `aaai.sty` - Estilo AAAI
- `aaai.bst` - Estilo de bibliografia
- `fixbib.sty` - Correções de bibliografia
- `formatting-instructions-latex.tex` - Exemplo/template

✅ **Extensão LaTeX Workshop**: Instalada no Cursor/VSCode
- Extensão: [LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop)

❌ **LaTeX não instalado**: `pdflatex` não encontrado no sistema

---

## 🔧 INSTALAÇÃO DO LATEX

### Requisitos (segundo documentação oficial)

A extensão LaTeX Workshop requer:
1. **LaTeX instalado** (TeX Live, MiKTeX, ou MacTeX)
2. **VSCode/Cursor versão 1.96.0 ou superior** (Dezembro 2024+)

### No WSL/Linux (TeX Live):

```bash
# Opção 1: Instalação completa (recomendada, mas demora ~30min)
sudo apt-get update
sudo apt-get install texlive-full

# Opção 2: Instalação básica (mais rápida, ~10min)
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-latex-recommended

# Opção 3: Instalação mínima (pode faltar pacotes)
sudo apt-get install texlive-latex-base
```

**Tempo estimado**: 
- Completa: ~30 minutos
- Básica: ~10 minutos

### Verificar instalação:

```bash
pdflatex --version
# Deve mostrar algo como: pdfTeX 3.14159265-2.6-1.40.21
```

---

## 📝 COMO USAR A EXTENSÃO LATEX WORKSHOP

### 1. Configuração Básica

A extensão LaTeX Workshop funciona **automaticamente** quando você:
- Abre um arquivo `.tex` no Cursor/VSCode
- A extensão detecta automaticamente o LaTeX instalado no PATH
- **Não precisa configuração adicional** na maioria dos casos!

### 2. Comandos Principais (segundo documentação oficial)

**Atalhos de Teclado:**
- `Ctrl+Alt+B` (Linux/Windows) ou `Cmd+Alt+B` (Mac): **Compilar** o documento
- `Ctrl+Alt+V` (Linux/Windows) ou `Cmd+Alt+V` (Mac): **Visualizar PDF** (aba interna)
- `Ctrl+Alt+J` (Linux/Windows) ou `Cmd+Alt+J` (Mac): **Visualizar PDF** no navegador externo

**Via Command Palette:**
- `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac) → Digite "LaTeX"
- Opções disponíveis:
  - `LaTeX Workshop: Build LaTeX project` - Compilar
  - `LaTeX Workshop: View LaTeX PDF` - Ver PDF
  - `LaTeX Workshop: Clean up auxiliary files` - Limpar arquivos temporários

### 3. Funcionalidades Automáticas

- ✅ **Compilação automática ao salvar** (configurável)
- ✅ **Visualização de PDF integrada** (painel lateral direito)
- ✅ **SyncTeX bidirecional**: Clique no PDF → vai para código fonte, e vice-versa
- ✅ **Autocomplete inteligente**: Comandos, ambientes, citações, referências
- ✅ **Erros e warnings destacados**: Problemas de compilação mostrados automaticamente
- ✅ **Snippets**: Digite `\` + nome do comando para autocompletar
- ✅ **Preview de equações**: Hover sobre equações para ver preview

---

## 📄 CRIAR ARQUIVO PRINCIPAL DO RELATÓRIO

Você precisa criar um arquivo `.tex` principal. Vou criar um template baseado no AAAI:

**Arquivo**: `relatorio.tex` ou `relatorio_tp2.tex`

---

## ⚙️ CONFIGURAÇÃO RECOMENDADA

### Arquivo `.vscode/settings.json` (opcional, mas recomendado):

```json
{
    "latex-workshop.latex.recipes": [
        {
            "name": "pdflatex",
            "tools": [
                "pdflatex"
            ]
        }
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ],
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.latex.autoClean.run": "onBuilt",
    "latex-workshop.latex.clean.fileTypes": [
        "*.aux",
        "*.bbl",
        "*.blg",
        "*.idx",
        "*.ind",
        "*.lof",
        "*.lot",
        "*.out",
        "*.toc",
        "*.acn",
        "*.acr",
        "*.alg",
        "*.glg",
        "*.glo",
        "*.gls",
        "*.fls",
        "*.log",
        "*.fdb_latexmk",
        "*.snm",
        "*.nav",
        "*.synctex.gz"
    ]
}
```

---

## 🚀 FLUXO DE TRABALHO COMPLETO

### Passo 1: Instalar LaTeX (se necessário)
```bash
# Verificar se já está instalado
pdflatex --version

# Se não estiver, instalar:
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### Passo 2: Abrir arquivo .tex no Cursor/VSCode
- Abra o arquivo `relatorio_tp2.tex` (ou crie um novo)
- A extensão LaTeX Workshop será ativada automaticamente

### Passo 3: Compilar o documento
- **Método 1**: Pressione `Ctrl+Alt+B`
- **Método 2**: `Ctrl+Shift+P` → "LaTeX Workshop: Build LaTeX project"
- **Método 3**: Salvar o arquivo (se auto-build estiver ativado)

### Passo 4: Visualizar PDF
- **Método 1**: Pressione `Ctrl+Alt+V` (visualização interna)
- **Método 2**: `Ctrl+Alt+J` (visualização no navegador)
- O PDF aparecerá no painel lateral direito

### Passo 5: Usar SyncTeX
- **Código → PDF**: Clique em uma linha no código, pressione `Ctrl+Alt+V`, o PDF mostrará a posição correspondente
- **PDF → Código**: Clique em uma posição no PDF, o código será destacado

### Passo 6: Editar e recompilar
- Faça alterações no arquivo `.tex`
- Salve (`Ctrl+S`) - se auto-build estiver ativo, compila automaticamente
- Ou compile manualmente com `Ctrl+Alt+B`
- O PDF será atualizado automaticamente

---

## ⚠️ PROBLEMAS COMUNS

### 1. "pdflatex não encontrado"
**Solução**: Instalar LaTeX (veja seção acima)

### 2. "Package not found"
**Solução**: Instalar pacotes faltantes
```bash
sudo apt-get install texlive-latex-extra
```

### 3. PDF não aparece
**Solução**: Verificar se compilação foi bem-sucedida
- Olhar o painel "Problems" no VSCode
- Verificar o arquivo `.log` gerado

### 4. Erros de compilação
**Solução**: 
- Ler mensagens de erro no painel "Problems"
- Verificar sintaxe LaTeX
- Verificar se todos os arquivos necessários estão presentes

---

## 📚 RECURSOS ÚTEIS

- [Documentação LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop/wiki)
- [Overleaf - Editor LaTeX Online](https://www.overleaf.com/) (alternativa se LaTeX não funcionar localmente)
- [LaTeX Tutorial](https://www.latex-tutorial.com/)

---

## ✅ CHECKLIST

- [ ] Instalar LaTeX no sistema
- [ ] Verificar instalação (`pdflatex --version`)
- [ ] Criar arquivo principal `.tex`
- [ ] Testar compilação
- [ ] Configurar extensão (opcional)
- [ ] Começar a escrever relatório

