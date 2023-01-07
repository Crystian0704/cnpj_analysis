# Acesso aos dados de CNPJ


## 1. Aquisição dos dados

Este código tem como objetivo baixar arquivos zip com os dados de CNPJ disponibilizados pelo governo brasileiro na página https://dadosabertos.rfb.gov.br/CNPJ/.

Ele possui as seguintes funções:

get_link(url: str) -> Optional[List[str]]: essa função é responsável por obter os links para download dos arquivos zip. Ela recebe como parâmetro a url da página da Receita Federal e retorna uma lista de links para download ou None em caso de falha na conexão.

download_zip(download_link: List[str]) -> None: essa função é responsável por realizar o download dos arquivos zip. Ela recebe como parâmetro uma lista de links de download e faz o download de cada arquivo, salvando-o na pasta "data/raw". Caso ocorra algum erro de conexão ou o usuário interrompa o processo, todos os arquivos zip já baixados serão removidos da pasta "data/raw".

No trecho de código if __name__ == '__main__', é realizada a chamada da função get_link() para obter os links de download, que são passados como parâmetro para a função download_zip(). Caso nenhum link seja encontrado, uma mensagem de erro é escrita no log.


