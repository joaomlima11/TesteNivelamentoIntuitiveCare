CREATE TABLE demonstracoes_contabeis (
    id INT PRIMARY KEY,
    ano INT NOT NULL,
    operadora_codigo VARCHAR(20) NOT NULL,
    descricao VARCHAR(255),
    valor DECIMAL(15,2),
    data_importacao DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE operadoras_ativas (
    id INT PRIMARY KEY,
    registro_ans VARCHAR(20) UNIQUE NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2),
    data_registro DATE,
    data_importacao DATETIME DEFAULT CURRENT_TIMESTAMP
);
BULK INSERT operadoras_ativas
FROM '/caminho/para/operadoras_ativas.csv'
WITH (
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
)
declare @data_registro unknown;
SET data_registro = STR_TO_DATE(@data_registro, '%d/%m/%Y');
COPY operadoras_ativas(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, uf, data_registro)
FROM 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/.csv'
DELIMITER ';' CSV HEADER;
SELECT o.razao_social, d.ano, SUM(d.valor) AS total
FROM demonstracoes_contabeis d
JOIN operadoras_ativas o ON d.operadora_codigo = o.registro_ans
GROUP BY o.razao_social, d.ano
ORDER BY total DESC;
