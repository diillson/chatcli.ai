<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/chatcli-logo-dark.png" />
    <img src="images/chatcli-logo.png" alt="ChatCLI" width="240" />
  </picture>
</p>

<h1 align="center">ChatCLI Documentation</h1>

<p align="center">
  <strong>Documentação oficial do ChatCLI — sua CLI de IA para o terminal.</strong>
</p>

<p align="center">
  <a href="https://chatcli.edilsonfreitas.com"><img src="https://img.shields.io/badge/docs-chatcli.edilsonfreitas.com-2563EB?style=for-the-badge&amp;logo=readthedocs&amp;logoColor=white" alt="Documentation" /></a>
  <a href="https://github.com/diillson/chatcli"><img src="https://img.shields.io/badge/source-diillson%2Fchatcli-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="GitHub" /></a>
</p>

<p align="center">
  <a href="https://github.com/diillson/chatcli/releases"><img src="https://img.shields.io/github/v/release/diillson/chatcli?style=flat-square&amp;color=2563EB&amp;label=latest%20release" alt="Latest Release" /></a>
  <a href="https://github.com/diillson/chatcli/stargazers"><img src="https://img.shields.io/github/stars/diillson/chatcli?style=flat-square&amp;color=F59E0B" alt="GitHub Stars" /></a>
  <a href="https://github.com/diillson/chatcli/issues"><img src="https://img.shields.io/github/issues/diillson/chatcli?style=flat-square&amp;color=EF4444" alt="Open Issues" /></a>
  <a href="https://github.com/diillson/chatcli"><img src="https://img.shields.io/github/go-mod/go-version/diillson/chatcli?style=flat-square&amp;color=00ADD8&amp;logo=go&amp;logoColor=white" alt="Go Version" /></a>
  <a href="https://github.com/diillson/chatcli/blob/main/LICENSE"><img src="https://img.shields.io/github/license/diillson/chatcli?style=flat-square&amp;color=7C3AED" alt="License" /></a>
  <a href="https://github.com/diillson/chatcli/actions"><img src="https://img.shields.io/github/actions/workflow/status/diillson/chatcli/3-publish-release.yml?style=flat-square&amp;label=CI&amp;logo=githubactions&amp;logoColor=white" alt="CI Status" /></a>
  <a href="https://github.com/diillson/chatcli/actions/workflows/security-scan.yml"><img src="https://img.shields.io/github/actions/workflow/status/diillson/chatcli/security-scan.yml?style=flat-square&amp;label=security%20scan&amp;logo=githubactions&amp;logoColor=white&amp;color=2DD4BF" alt="Security Scan" /></a>
  <img src="https://img.shields.io/badge/Trivy-image%20scanning-00C9A7?style=flat-square&amp;logo=aquasecurity&amp;logoColor=white" alt="Trivy" />
  <img src="https://img.shields.io/badge/Sigstore-cosign%20signed-4B32C3?style=flat-square&amp;logo=sigstore&amp;logoColor=white" alt="Cosign Signed" />
</p>

---

## Sobre

Este repositório contém a **documentação oficial** do [ChatCLI](https://github.com/diillson/chatcli), construída com [Mintlify](https://mintlify.com) e publicada em **[chatcli.edilsonfreitas.com](https://chatcli.edilsonfreitas.com)**.

O ChatCLI é uma CLI open-source escrita em Go que leva os principais provedores de LLM para o terminal, com coder mode, agentes, servidor gRPC, operator Kubernetes e muito mais. A lista de provedores e modelos fica em [Modelos suportados](https://chatcli.edilsonfreitas.com/providers/supported-models).

---

## Estrutura da Documentação

O inglês é servido na raiz e o português em `pt/`, com a mesma árvore. A navegação (`docs.json`) segue as seções abaixo.

```
chatcli.ai/
├── index.mdx                   # Home: banner, release mais recente, início rápido
├── start/                      # Comece aqui: quickstart, instalação, Docker/K8s, atualização
├── usage/                      # Usando o ChatCLI: prompt, @contexto, modos agent/coder, one-shot
├── coder/                      # Coder: @coder, tools atômicos, permissões, worktrees, LSP
├── agents/                     # Agentes: multiagente, squad, task graph, personas
│   └── harness/                #   Harness de qualidade (7 padrões + evals)
├── context/                    # Contexto e memória: contexto persistente, knowledge, sessões
├── providers/                  # Modelos e provedores: catálogo, OAuth, Bedrock, fallback, custo
├── tools/                      # Ferramentas: web, browser, API explorer, forges, imagens, scheduler
├── extensions/                 # Extensões: plugins, MCP, skills, slash commands, hooks
├── gateway/                    # Canais e gateway: Telegram, Slack, Discord, WhatsApp, voz
├── server/                     # Servidor e IDE: gRPC, conexão remota, servidor MCP, ACP
├── kubernetes/                 # Kubernetes e AIOps: watcher, operator
│   └── aiops/                  #   Plataforma AIOps
├── security/                   # Segurança
├── cookbook/                   # Receitas passo a passo
├── reference/                  # Comandos, variáveis, configuração, arquitetura, API REST
├── releases.mdx                # Índice das notas de release (gerado)
├── releases/                   # Uma página por versão (gerado)
├── help/                       # Troubleshooting e contribuição
├── pt/                         # A mesma árvore em português
├── images/                     # Logos, favicon, ícone do ArtifactHub, mídia
├── scripts/gen-intro-banner.py # Gera o banner da home a partir do cli/welcome.go
├── style.css                   # Tema: tokens de cor claro/escuro, componentes, home, releases
├── flags.js                    # Bandeiras no seletor de idioma
└── docs.json                   # Configuração e navegação do Mintlify
```

### Notas de release (geradas)

`releases.mdx`, `releases/`, a faixa "New release" da home (entre os marcadores `release-strip`) e o grupo Releases da navegação são gerados a partir do `CHANGELOG.md` do release-please pelo `scripts/docs/gen-release-notes.py` do repositório do ChatCLI. O job `update_docs_version` da pipeline de release roda o script a cada versão; edições à mão nesses arquivos são sobrescritas. Para regenerar localmente:

```bash
python3 ../chatcli/scripts/docs/gen-release-notes.py \
  --changelog ../chatcli/CHANGELOG.md --docs .
```

---

## Desenvolvimento Local

### Pré-requisitos

- [Node.js](https://nodejs.org/) v18+
- [Mintlify CLI](https://www.npmjs.com/package/mint) (`mint`)

### Executar localmente

```bash
# Instalar a CLI do Mintlify
npm i -g mint

# Clonar o repositório
git clone https://github.com/diillson/chatcli.ai.git
cd chatcli.ai

# Iniciar servidor de desenvolvimento (as ~840 páginas de release pedem
# mais memória para o Node)
NODE_OPTIONS=--max-old-space-size=8192 mint dev
```

O site estará disponível em `http://localhost:3000`.

### Adicionar nova página

1. Crie o arquivo `.mdx` na seção apropriada, em inglês na raiz e em português em `pt/`
2. Adicione o path nos dois idiomas em `docs.json`, na seção `navigation`
3. Verifique localmente com `mint dev` e `mint broken-links`

---

## Deploy

O deploy é **automático** via Mintlify. A cada push na branch `main`, o site é reconstruído e publicado em:

> **https://chatcli.edilsonfreitas.com**

A busca (search index) é atualizada automaticamente após cada deploy.

---

## Tecnologias

| Tech | Uso |
|:---|:---|
| [Mintlify](https://mintlify.com) | Framework de documentação |
| MDX | Markdown + JSX para componentes interativos |
| Tabs, Steps, Cards, Accordions | Componentes visuais do Mintlify |
| Busca instantânea | Indexação automática do Mintlify |

---

## Contribuindo

Contribuições são bem-vindas! Para melhorias na documentação:

1. Fork o repositório
2. Crie uma branch (`git checkout -b docs/minha-melhoria`)
3. Faça suas alterações
4. Teste com `mint dev` e `mint broken-links`
5. Abra um Pull Request

Para contribuir com o **código do ChatCLI**, veja o [repositório principal](https://github.com/diillson/chatcli).

---

## Links

| | Link |
|:---|:---|
| Documentação | [chatcli.edilsonfreitas.com](https://chatcli.edilsonfreitas.com) |
| Código-fonte | [github.com/diillson/chatcli](https://github.com/diillson/chatcli) |
| Releases | [github.com/diillson/chatcli/releases](https://github.com/diillson/chatcli/releases) |
| Issues | [github.com/diillson/chatcli/issues](https://github.com/diillson/chatcli/issues) |

---

<p align="center">
  Feito com 💙 por <a href="https://github.com/diillson">Edilson Freitas</a>
</p>
