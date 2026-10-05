
Este é um schedule interno rodando em produção, que atualiza automaticamente uma planilha no google sheets com gspread, com o resultado
de uma consulta no banco de dados Oracle.

A interface gráfica para monitoramento com cronometro e gráfico de execuções foi criada em Streamlit

##Como configurar google cloud API

- Google cloud > Ctrl + O > Novo projeto > Selecione o projeto
- Aperte "." (ponto) no teclado > APIs e serviços > Biblioteca
- Na barra de pesquisa procure por "Google drive API" > ative a API > Pesquise por "Google Sheets API" > ative a API
- APIs e serviços > Credenciais > Gerenciar contas de serviço > Criar conta de serviço

Um json com as credenciais será baixado automaticamente no navegador após a conta ser criada.
Já pode fechar o google cloud.

No google sheets, crie uma planila, nomeie a planilha e salve num bloco de notas o ID da planilha.
https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/edit?gid=0#gid=0

Compartilhe a planilha com o email da conta de serviço
Normalmente vem no formato googlesheetsserviceaccount@vocal-door-######-a1.iam.gserviceaccount.com

Crie um arquivo chamado credentials.json na pasta secrets, e cole no arquivo o json baixado. 
Crie um arquivo chamado db_credentials.json e faça um json com as credenciais necessárias para se conectar ao banco