# 📓 Miniguia de Estudos: Arquitetura de Microsserviços com NotebookLM

## 🎯 Contexto e Objetivos
Este repositório foi criado como parte de um desafio de projeto na DIO (Digital Innovation One). O objetivo principal é explorar o potencial do **NotebookLM** (ferramenta de IA do Google baseada no Gemini) como um assistente de aprendizagem ativa e curadoria de conhecimento.

* **Tema Escolhido:** Arquitetura de Microsserviços vs. Monólitos.
* **Objetivo de Estudo:** Compreender os padrões de design de microsserviços, quando adotar essa arquitetura, as principais vantagens (escalabilidade, deploy independente) e os desafios gerados (complexidade de rede, consistência de dados).

---

## 📚 Curadoria de Fontes
Para alimentar o NotebookLM e garantir respostas precisas e sem alucinações, foram selecionadas as seguintes fontes abertas e artigos técnicos:

1. **Artigo Base:** *Microservices Guide* por Martin Fowler (Disponível publicamente em martinfowler.com)
2. **Artigo Técnico:** *Pattern: Microservice Architecture* (Disponível em microservices.io)
3. **Whitepaper:** *Architecting Cloud-Native Applications on AWS* (PDF público da AWS)
4. **Documentação:** *Introduction to Microservices* (Nginx Architecture Guide)

---

## 🧠 Engenharia de Prompts e "Cicatrizes" (Troubleshooting)
Aqui está o registro do processo de iteração com a IA para extrair os melhores insights das fontes fornecidas.

### 🧪 Teste de Prompt 1: Abordagem Direta (Genérica)
* **Prompt enviado:** *"Me explique o que são microsserviços."*
* **Resultado:** A IA trouxe uma resposta correta, porém muito genérica e superficial, parecida com qualquer busca no Google. Não aproveitou o potencial dos PDFs carregados.

### 🎯 Teste de Prompt 2: Engenharia de Prompt (Específica + Contexto)
* **Prompt enviado:** 
  > "Agindo como um Arquiteto de Software Sênior, analise os documentos de Martin Fowler e AWS que enviei. Resuma os 3 principais trade-offs (vantagens e desvantagens) de migrar um sistema monolítico para microsserviços. Cite em qual página ou documento você encontrou essa informação."
* **Resultado:** Excelente. A IA estruturou a resposta em tópicos, destacando a complexidade de rede versus a velocidade de deploy, citando diretamente os trechos dos artigos do Fowler.

### 🪵 Cicatrizes e Solução de Problemas (Troubleshooting)
* **Dificuldade encontrada:** Inicialmente, o NotebookLM misturou conceitos de microsserviços com metodologias ágeis (Scrum), pois uma das fontes citava a organização dos times (Two-Pizza Teams da Amazon).
* **Como resolvi (Ajuste de Raciocínio):** Apliquei um prompt de restrição: *"Foque estritamente na perspectiva técnica e de infraestrutura. Desconsidere a divisão organizacional de equipes no momento."* Isso limpou o ruído da resposta.

---

## 📖 Miniguia de Estudo (Entrega Final)

### 📌 Resumo Estruturado do Assunto
A arquitetura de microsserviços consiste em abordar o desenvolvimento de software através de pequenos serviços independentes que se comunicam via protocolos leves (como HTTP/REST ou mensageria com RabbitMQ/Kafka). 

* **Monólitos:** Mais fáceis de testar e buildar no início, mas tornam-se gigantes difíceis de escalar.
* **Microsserviços:** Permitem que cada parte do sistema cresça de forma independente, utilizando tecnologias diferentes se necessário, mas exigem alta maturidade de DevOps (CI/CD, Observabilidade).

### 🗂️ Glossário de Conceitos Chave
* **API Gateway:** O ponto de entrada único para todas as requisições dos clientes, distribuindo-as para os microsserviços corretos.
* **Service Discovery:** Mecanismo automático para detectar em qual endereço IP/porta um microsserviço está rodando na rede.
* **Circuit Breaker:** Padrão de design que impede que a falha de um serviço derrube todo o ecossistema (evita falhas em cascata).
* **Event-Driven Architecture:** Padrão onde os serviços se comunicam reagindo a eventos (ex: "Pedido Criado"), reduzindo o acoplamento direto.

### 🔄 Prompts Reutilizáveis para Revisão Futura
Você pode copiar e colar estes prompts no seu NotebookLM para revisar este tema futuramente:

* `Prompt de Flashcards:` *"Com base nos documentos fornecidos, crie 5 perguntas e respostas no estilo flashcard para testar meu conhecimento sobre resiliência em microsserviços."*
* `Prompt de Estudo de Caso:` *"Crie um cenário hipotético de uma falha de sistema em uma arquitetura de microsserviços de e-commerce e me pergunte como eu resolveria usando os conceitos do glossário."*

---
🎨 Projeto desenvolvido por Gabriele Quevedo para o Desafio de Projeto na [DIO](https://www.dio.me).