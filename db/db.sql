-- database -- 
create database sistema_condominio;
use sistema_condominio;
-- tabelas --
create table usuarios(
    id int not null auto_increment primary key,
    nome varchar(255),
    idade int,
    cpf varchar(14) unique,
    telefone varchar(20),
    data_nasc date
);
-- necessidade de uma tabela de login --
create table login(
    id int not null auto_increment primary key,
    id_user int,
    ilogin varchar(255) unique,
    senha varchar(64),
    tipo_acesso enum("morador", "visitante", "funcionario", "admin") not null default 'morador',
    foreign key (id_user) references usuarios(id)
);
create table apartamentos(
    id int not null auto_increment primary key,
    numero int,
    descricao varchar(255)
);
create table veiculos(
    id int not null auto_increment primary key,
    id_usuario int,
    placa varchar(10),
    descricao varchar(255),
    documento varchar(255),
    foreign key (id_usuario) references usuarios(id)
);
create table estacionamento(
    id int not null auto_increment primary key,
    numero int
);
create table funcionarios(
    id int not null auto_increment primary key,
    id_user int,
    id_veiculo int,
    id_vaga int,
    descricao varchar(255),
    foreign key (id_user) references usuarios(id),
    foreign key (id_veiculo) references veiculos(id),
    foreign key (id_vaga) references estacionamento(id)
);
create table moradores(
    id int not null auto_increment primary key,
    id_user int,
    id_veiculo int,
    id_vaga int,
    id_apto int,
    foreign key (id_user) references usuarios(id),
    foreign key (id_veiculo) references veiculos(id),
    foreign key (id_vaga) references estacionamento(id),
    foreign key (id_apto) references apartamentos(id)
);
create table visitantes(
    id int not null auto_increment primary key,
    id_user int,
    id_veiculo int,
    id_vaga int,
    id_morador int,
    foreign key (id_user) references usuarios(id),
    foreign key (id_veiculo) references veiculos(id),
    foreign key (id_vaga) references estacionamento(id),
    foreign key (id_morador) references moradores(id)
);
create table ocorrencias(
    id int not null auto_increment primary key,
    id_usuario int,
    descricao varchar(255),
    foreign key (id_usuario) references usuarios(id)
);
create table encomendas(
    id int not null auto_increment primary key,
    id_usuario int,
    descricao varchar(255),
    data_entrega date,
    data_coleta date,
    foreign key (id_usuario) references usuarios(id)
);
create table notificacoes(
    id int not null auto_increment primary key,
    id_usuario int,
    descricao varchar(255),
    foreign key (id_usuario) references usuarios(id)
);
-- inserts --