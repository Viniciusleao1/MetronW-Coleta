-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 24/08/2024 às 02:41
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `metronw-coleta`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `aguardando`
--

CREATE TABLE `aguardando` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `mensagem_id` int(11) DEFAULT NULL,
  `last_message` text DEFAULT NULL,
  `data_criacao` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `aguardando`
--

INSERT INTO `aguardando` (`id`, `usuario_id`, `mensagem_id`, `last_message`, `data_criacao`) VALUES
(1, 213, 216, 'os equipamentos foram configurados por nós? Teria o número do ticket desta configuração se sim?', '2024-08-23 13:49:45'),
(2, 211, 211, 'Testando', '2024-08-23 13:13:31'),
(4, 211, 211, 'Finalizando testes', '2024-08-23 13:13:31'),
(6, 213, 216, 'Lá será o POP T36  - IBIRAPUÃ', '2024-08-23 13:49:45'),
(7, 211, 211, 'Finalizando testes', '2024-08-23 13:13:31'),
(9, 211, 211, 'Analise', '2024-08-23 13:13:31'),
(10, 211, 211, 'Análise secundária', '2024-08-23 13:13:31'),
(11, 211, 211, 'Testando 2', '2024-08-23 13:13:31'),
(12, 211, 211, 'Teste', '2024-08-23 13:13:31');

-- --------------------------------------------------------

--
-- Estrutura para tabela `mensagens`
--

CREATE TABLE `mensagens` (
  `id` int(11) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `last_message` text DEFAULT NULL,
  `data_criacao` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `mensagens`
--

INSERT INTO `mensagens` (`id`, `ticket_id`, `status`, `last_message`, `data_criacao`) VALUES
(210, 0, 'pending', 'Testando', '2024-08-23 13:13:31'),
(211, 211, 'pending', 'Teste', '2024-08-23 13:13:31'),
(212, 216, 'pending', 'tudo certo ?', '2024-08-23 14:23:31'),
(216, 213, 'pending', 'Lá será o POP T36  - IBIRAPUÃ', '2024-08-23 13:49:45');

-- --------------------------------------------------------

--
-- Estrutura para tabela `quantidades`
--

CREATE TABLE `quantidades` (
  `id` int(11) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `quantidades`
--

INSERT INTO `quantidades` (`id`, `ticket_id`, `quantidade`, `timestamp`) VALUES
(1, 0, 28, '2024-08-24 00:35:52');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id`, `nome`) VALUES
(211, 'Metro X Free'),
(213, 'TECNET/METRO CSE'),
(216, 'Mendex / CSE');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `aguardando`
--
ALTER TABLE `aguardando`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `mensagem_id` (`mensagem_id`);

--
-- Índices de tabela `mensagens`
--
ALTER TABLE `mensagens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticket_id` (`ticket_id`);

--
-- Índices de tabela `quantidades`
--
ALTER TABLE `quantidades`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticket_id` (`ticket_id`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `aguardando`
--
ALTER TABLE `aguardando`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `mensagens`
--
ALTER TABLE `mensagens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=237;

--
-- AUTO_INCREMENT de tabela `quantidades`
--
ALTER TABLE `quantidades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=217;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `aguardando`
--
ALTER TABLE `aguardando`
  ADD CONSTRAINT `aguardando_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `aguardando_ibfk_2` FOREIGN KEY (`mensagem_id`) REFERENCES `mensagens` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
