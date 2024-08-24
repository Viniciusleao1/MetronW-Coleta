-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 24/08/2024 às 05:20
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
  `grupo_id` int(11) DEFAULT NULL,
  `mensagens_nao_lidas` int(11) DEFAULT NULL,
  `ultima_mensagem` text DEFAULT NULL,
  `data_ultima_mensagem` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `data_criacao` timestamp NOT NULL DEFAULT current_timestamp(),
  `data_atualizacao` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `conversas` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `aguardando`
--

INSERT INTO `aguardando` (`id`, `grupo_id`, `mensagens_nao_lidas`, `ultima_mensagem`, `data_ultima_mensagem`, `data_criacao`, `data_atualizacao`, `conversas`) VALUES
(1, 211, 32, 'Analisando conversas', '2024-08-24 03:12:33', '2024-08-24 02:41:17', '2024-08-24 03:12:33', '5'),
(6, 225, 61, 'Prezado Cliente, caso não venha lhe responder em tempo hábil, favor contatar nossos canais oficiais de atendimento: WhatsApp (através de seu canal), WhatsApp (047) 3047-8400, E-mail (cse@metronetwork.com.br) ou Telefone (047) 3047-8400. Somos gratos pela sua compreensão e apoio.', '2024-08-24 06:11:11', '2024-08-24 03:12:33', '2024-08-24 03:19:43', '5');

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
  ADD UNIQUE KEY `grupo_id` (`grupo_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=217;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
