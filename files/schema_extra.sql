-- LibrasCode: tabelas dos 2 novos requisitos (questões + pontuação)
-- Rode no MySQL, no mesmo banco que você já usa (USE et;)

-- A tabela librascode deve ter idlibrascode como chave primária.
-- Confira com:  DESCRIBE librascode;
-- Se não tiver essa coluna, ajuste a tabela antes de criar as respostas.

CREATE TABLE IF NOT EXISTS modulos (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(50)  NOT NULL,
    descricao VARCHAR(150),
    ordem     INT NOT NULL DEFAULT 0
);

-- Cada sinal = uma palavra + o arquivo (png/jpg/gif) que mostra o sinal.
-- As questões são GERADAS a partir desta tabela: quanto mais sinais, mais questões.
CREATE TABLE IF NOT EXISTS sinais (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    modulo_id INT NOT NULL,
    palavra   VARCHAR(40)  NOT NULL,
    midia     VARCHAR(100) NOT NULL,
    FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
);

-- Cada resposta dada pelo usuário. A pontuação é a soma da coluna pontos.
CREATE TABLE IF NOT EXISTS respostas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id    INT NOT NULL,
    sinal_id      INT NOT NULL,
    acertou       TINYINT(1) NOT NULL,
    pontos        INT NOT NULL DEFAULT 0,
    respondida_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES librascode(idlibrascode) ON DELETE CASCADE,
    FOREIGN KEY (sinal_id)   REFERENCES sinais(id)             ON DELETE CASCADE
);

-- Dados de exemplo (troque pelos sinais que você realmente tiver em mídia)
INSERT INTO modulos (nome, descricao, ordem) VALUES
    ('Saudações',   'Cumprimentos do dia a dia', 1),
    ('Família',     'Membros da família',        2),
    ('Programação', 'Termos de computação',      3);

INSERT INTO sinais (modulo_id, palavra, midia) VALUES
    (1, 'Oi',        'oi.gif'),
    (1, 'Obrigado',  'obrigado.gif'),
    (1, 'Tchau',     'tchau.gif'),
    (1, 'Por favor', 'por_favor.gif'),
    (2, 'Mãe',       'mae.gif'),
    (2, 'Pai',       'pai.gif'),
    (2, 'Irmão',     'irmao.gif'),
    (2, 'Filho',     'filho.gif'),
    (3, 'Computador','computador.gif'),
    (3, 'Tecnologia','tecnologia.gif'),
    (3, 'Internet',  'internet.gif'),
    (3, 'Rede',      'rede.gif')