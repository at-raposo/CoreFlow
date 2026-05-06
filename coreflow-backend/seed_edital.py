import re
from app.core.database import SessionLocal
from app.models.taxonomy import Edital, Topic, Tag

text_cargo_4 = """1 Fundamentos da computação. 1.1 Organização e arquitetura de computadores. 1.2 Sistemas operacionais: arquiteturas e componentes. 1.2.1 Kernel. 1.2.2 Gerenciador de memória. 1.2.3 Gerenciador de arquivos. 1.2.4 Gerenciador de E/S. 1.2.5 Middleware. 1.3 Processadores. 1.3.1 Arquiteturas paralelas: Multiprocessamento e Multicore. 1.3.2 Hyper-Threading. 1.3.3 GPUs: arquitetura CUDA e aplicações em processamento vetorial. 1.4 Sistemas Distribuídos. 1.4.1 Modelos de memória compartilhada. 1.5 Tecnologias de virtualização: emuladores, máquinas virtuais, contêineres. 1.6 RAID: tipos, características e aplicações. 1.7 Sistemas de arquivos NTFS, FAT32, exFAT, EXT3, EXT4, XFS: características, organização e metadados. 1.8 Computação quântica: conceitos envolvidos. 
2 Bancos de dados. 2.1 Arquitetura, modelos lógicos e representação física. 2.2 Bancos de dados multidimensionais: conceitos envolvidos. 2.3 SGBDs relacionais. 2.3.1 SQLite. 2.4 Linguagem de consulta estruturada (SQL). 2.5 Transações: características e análise de logs. 2.6 NOSQL. 
3 Engenharia reversa de software. 3.1 Técnicas e ferramentas de descompilação de programas. 3.2 Debuggers. 3.3 Análise de código malicioso: vírus, backdoors, keyloggers, worms e outros. 3.4 Ofuscação de código. 3.5 Compactadores de código executável. 3.6 Malware polimórfico. 3.7 Técnicas de sandboxing. 3.8 Linguagem Assembly. 
4 Linguagens de programação. 4.1 Noções de linguagens de programação orientadas a objetos: objetos, classes, herança, polimorfismo, sobrecarga de métodos. 4.2 Noções de linguagens procedurais: tipos de dados elementares e estruturados, funções e procedimentos. 4.3 Estruturas de controle de fluxo de execução. 4.4 Montadores, compiladores, ligadores e interpretadores. 4.5 Linguagens C, Java, Javascript e Python. 4.6 Desenvolvimento Web: HTML, XML, JSON, APIs REST/GraphQL. 4.7 Análise estática de código fonte: SonarQube. 
5 Estruturas de dados e algoritmos. 5.1 Estruturas de dados: listas, filas, pilhas e árvores. 5.2 Métodos de acesso, busca, inserção e ordenação em estruturas de dados. 5.3 Complexidade de algoritmos. 5.4 Autômatos determinísticos e não-determinísticos. 
6 Redes de computadores. 6.1 Tipos, tecnologias e topologias de redes de computadores. 6.2 Técnicas básicas de comunicação. 6.3 Técnicas de comutação de circuitos, pacotes e células. 6.4 Elementos de interconexão: gateways, hubs, repetidores, bridges, switches, roteadores. 6.5 Arquiteturas e protocolos de redes. 6.5.1 Modelo OSI e arquitetura TCP/IP. 6.5.2 Arquitetura cliente-servidor. 6.5.3 Ethernet. 6.5.4 . Redes peer-to-peer (P2P). 6.5.5 Comunicação sem fio: padrões 802.11, Bluetooth. 6.5.6 Redes móveis de dados (celular). 6.5.7 Protocolos IP, TCP, UDP, SCTP, ARP, TLS, SSL, OSPF, BGP, DNS, DHCP, ICMP, FTP, SFTP, SSH, HTTP, HTTPS, SMTP, IMAP, POP3. 6.6 Redes TOR. 6.7 Computação em nuvem. 
7 Segurança da informação. 7.1 Normas NBR ISO/IEC nº 27001:2022 e nº 27002:2022. 7.2 Desenvolvimento seguro de aplicações: SDL, CLASP e OWASP Top 10. 7.3 Segurança de contêineres: Docker, Kubernetes e runtime security. 7.4 Autenticação e Autorização: características, fundamentos e conceitos envolvidos. 7.4.1 Single Sign-On (SSO), SAML, OAuth 2.0, OpenId Connect (OIDC). 7.4.2 Biometria comportamental, reconhecimento facial, análise de íris, voz, impressão digital. 7.4.3 Protocolos de autenticação sem senha: FIDO2/WebAuthn. 7.4.4 Múltiplos Fatores de Autenticação (MFA). 7.5 Malware: virus, keylogger, trojan, spyware, backdoor, worms, rootkit, adware, fileless, ransomware. 7.6 OSINT. 7.7 Esteganografia. 7.8 Recuperação de dados. 7.8.1 Principais técnicas de recuperação de arquivos apagados em sistemas de arquivos. 7.8.2 Ambientes de nuvem: AWS, Azure e Google Cloud. 
8 Segurança de redes de computadores. 8.1 Firewall, sistemas de prevenção e detecção de intrusão (IPS e IDS), antivírus, EDR, XDR, SOAR, SIEM, NAT, proxy, VPN. 8.2 Protocolos IPSEC, DNSSEC, DMARC, DKIM, SPF. 8.3 Monitoramento e análise de tráfego: sniffers, traffic shaping. 8.4 Segurança de redes sem fio: EAP, WEP, WPA, WPA2, WPA3, autenticação baseada em contexto, protocolo 802.1X. 8.5 Ataques a redes de computadores. 8.5.1 DoS, DDoS, botnets, phishing, zero-day exploits, ping da morte, UDP Flood, MAC flooding, IP spoofing, ARP spoofing, buffer overflow, SQL injection, Cross-Site Scripting (XSS), DNS Poisoning. 8.5.2 MITRE ATT&CK. 8.6. Frameworks de segurança da informação e segurança cibernética: CIS Controls e NIST CyberSecurity Framework (CSF). 8.7 Ameaças persistentes avançadas (APTs). 
9 Criptografia. 9.1 Sistemas criptográficos simétricos e assimétricos. 9.2 Certificação digital. 9.3 Modos de operação de cifras. 9.4 Algoritmos RSA, AES, ECC, IDEA, Twofish, Blowfish, 3DES e RC4. 9.5 Protocolo Diffie–Hellman. 9.6 Hashes criptográficos: algoritmos MD5, SHA-1, SHA-2, SHA-3, colisões. 9.7 Técnicas: força bruta, criptoanálise, canal lateral, ataques de texto conhecido/escolhido, Man-in-the-Middle (MITM). 9.8 Protocolo Signal. 9.9 Blockchain. 9.10 Criptomoedas. 
10 Sistema Operacional Windows. 10.1 Sistemas Windows: 10/11, Server 2019/2022. 10.2 Gerenciamento de usuários e permissões de acesso. 10. 3 Log de eventos do Windows. 10.4 Registro do Windows. 
11 Sistema Operacional Linux. 11.1 Características do sistema operacional Linux. 11.2 Gerenciamento de usuários e permissões de acesso. 11.3 Configuração, administração e logs de sistema e de serviços: proxy, correio eletrônico, servidor Web, servidor de arquivos. 11.4 Shell e comandos. 
12 Sistemas operacionais móveis: Android e iOS. 12.1 Arquitetura. 12.2 Segurança: modelos de permissão, sandboxing, criptografia de dados. 12.3 Gerenciamento de memória e processos. 12.4 Sistemas de arquivos. 
13 Governança de TI e Legislação aplicada. 13.1 ITIL 4: características gerais. 13.2 Contratações de TI: Lei 14.133/2021, Instrução Normativa SGD/ME nº 94/2022. 13.3 Marco Civil da Internet (Lei nº 12.965/2014): Responsabilidades de provedores e coleta de logs. 
14 Inteligência Artificial. 14.1 Aprendizado de Máquina: supervisionado, não supervisionado, semi-supervisionado, aprendizado por reforço, análise preditiva. 14.2 Redes Neurais e Deep Learning. 14.3 LLMs e Processamento de linguagem natural. 14.4 Inteligência Artificial Generativa. 14.5 Deepfakes. 
15 Princípios da computação forense. 15.1 Os crimes cibernéticos e seus vestígios. 15.2 Identificação, isolamento, preservação e coleta de vestígio cibernético. 15.3 Principais exames realizados em computação forense."""

text_basico = """LÍNGUA PORTUGUESA: 1 Compreensão e interpretação de textos de gêneros variados. 2 Reconhecimento de tipos e gêneros textuais. 3 Domínio da ortografia oficial. 4 Domínio dos mecanismos de coesão textual. 4.1 Emprego de elementos de referenciação, substituição e repetição, de conectores e de outros elementos de sequenciação textual. 4.2 Emprego de tempos e modos verbais. 5 Domínio da estrutura morfossintática do período. 5.1 Emprego das classes de palavras. 5.2 Relações de coordenação entre orações e entre termos da oração. 5.3 Relações de subordinação entre orações e entre termos da oração. 5.4 Emprego dos sinais de pontuação. 5.5 Concordância verbal e nominal. 5.6 Regência verbal e nominal. 5.7 Emprego do sinal indicativo de crase. 5.8 Colocação dos pronomes átonos. 6 Reescrita de frases e parágrafos do texto. 6.1 Significação das palavras. 6.2 Substituição de palavras ou de trechos de texto. 6.3 Reorganização da estrutura de orações e de períodos do texto. 6.4 Reescrita de textos de diferentes gêneros e níveis de formalidade. 7 Correspondência oficial (conforme Manual de Redação da Presidência da República). 7.1 Aspectos gerais da redação oficial. 7.2 Finalidade dos expedientes oficiais. 7.3 Adequação da linguagem ao tipo de documento. 7.4 Adequação do formato do texto ao gênero.
INFORMÁTICA: 1 Componentes de um computador (hardware e software). 2 Noções de sistemas operacionais: Windows, Android e iOS. 3 Navegadores de Internet, webmail e ferramentas de produtividade do Microsoft Office 365. 4 Noções de segurança da informação. 4.1 Responsabilidades e deveres dos usuários de serviços de TI. 4.2 Malware: vírus, worms. 4.3 Phishing, baiting e engenharia social: métodos e canais utilizados. 4.4 Aplicativos para segurança: antivírus, Endpoint Detection and Response (EDR), firewall, anti-spyware, gerenciadores de senhas. 4.5 Múltiplos Fatores de Autenticação (MFA). 4.6 Assinatura e certificação digital. 5 Computação em nuvem: conceitos envolvidos, vantagens e desvantagens. 6 Noções de bancos de dados. 6.1 Conceitos básicos e características. 6.2 Dados estruturados e não estruturados. 6.3 Banco de dados relacionais. 6.4 Chaves e relacionamentos. 7 Noções de redes de computadores. 7.1 Tipos: locais (LAN), metropolitanas (MAN) e de longa distância (WAN). 7.2 Internet e Intranet. 7.3 Arquitetura TCP/IP, NAT. 7.4 Acesso remoto a computadores: VPN, RDP. 8 Noções de programação. 8.1 Linguagem Python. 8.2 Low-Code/No-Code. 9 Metadados de arquivos. 10 Noções de aprendizado de máquina. 10.1 Mineração de dados: conceituação e características. 10.2 Big data: conceito, premissas e aplicação. 10.3 IA Generativa: principais características.
NOÇÕES DE DIREITO ADMINISTRATIVO: 1 Noções de organização administrativa. 1.1 Centralização, descentralização, concentração e desconcentração. 1.2 Administração direta e indireta. 1.3 Autarquias, fundações, empresas públicas e sociedades de economia mista. 2 Ato administrativo. 2.1 Conceito, requisitos, atributos, classificação e espécies. 3 Agentes públicos. 3.1 Legislação pertinente. 3.1.1 Lei nº 8.112/1990 e suas alterações. 3.1.2 Disposições constitucionais aplicáveis. 3.2 Disposições doutrinárias. 3.2.1 Conceito. 3.2.2 Espécies. 3.2.3 Cargo, emprego e função pública. 4 Poderes administrativos. 4.1 Hierárquico, disciplinar, regulamentar e de polícia. 4.2 Uso e abuso do poder. 5 Licitação. 5.1 Princípios. 5.2 Contratação direta: dispensa e inexigibilidade. 5.3 Modalidades. 5.4 Tipos. 5.5 Procedimento. 6 Controle da Administração Pública. 6.1 Controle exercido pela Administração Pública. 6.2 Controle judicial. 6.3 Controle legislativo. 7 Responsabilidade civil do Estado. 7.1 Responsabilidade civil do Estado no direito brasileiro. 7.1.1 Responsabilidade por ato comissivo do Estado. 7.1.2 Responsabilidade por omissão do Estado. 7.2 Requisitos para a demonstração da responsabilidade do Estado. 7.3 Causas excludentes e atenuantes da responsabilidade do Estado. 8 Regime jurídico-administrativo. 8.1 Conceito. 8.2 Princípios expressos e implícitos da Administração Pública.
NOÇÕES DE DIREITO CONSTITUCIONAL: 1 Direitos e garantias fundamentais: direitos e deveres individuais e coletivos. 2 Poder Executivo: forma e sistema de governo. 3 Defesa do Estado e das instituições democráticas: segurança pública. 4 Ordem social.
NOÇÕES DE DIREITO PENAL E DE DIREITO PROCESSUAL PENAL: 1 Princípios básicos. 2 Aplicação da lei penal. 2.1 A lei penal no tempo e no espaço. 2.2 Tempo e lugar do crime. 2.3 Territorialidade e extraterritorialidade da lei penal. 3 O fato típico e seus elementos. 3.1 Crime consumado e tentado. 3.2 Ilicitude e causas de exclusão. 3.3 Excesso punível. 4 Crimes contra a pessoa. 5 Crimes contra o patrimônio. 6 Crimes contra a fé pública. 7 Crimes contra a Administração Pública. 8 Inquérito policial. 8.1 Histórico, natureza, conceito. 9 Prova. 9.1 Exame do corpo de delito e perícias em geral. 9.1.1 Perícias regulamentadas no CPP. 9.1.2 Requisição de perícia. 9.1.3 Formalidades e obrigações impostas ao perito. 9.1.4 Nova perícia e atuação do Assistente técnico. 9.2 Cadeia de custódia da prova. 9.2.1 Conceito de cadeia de custódia. 9.2.2 Importância da cadeia de custódia. 9.2.3 Etapas da cadeia de custódia. 9.2.4 Atores envolvidos com a cadeia de custódia. 9.2.5 Efeitos jurídicos da inobservância da cadeia de custódia da prova pericial. 9.3 Requisitos e ônus da prova. 9.4 Nulidade da prova. 9.5 Documentos de prova. 9.6 Reconhecimento de pessoas e coisas. 9.7 Acareação. 9.8 Indícios. 9.9 Busca e apreensão. 10 Restrição de liberdade. 10.1 Prisão em flagrante. 11. Função pericial do Estado e a perícia no contexto processual brasileiro. 11.1 A Perícia Criminal Federal. 11.2 Polícias Científicas Estaduais. 12 Lei nº 12.030.
NOÇÕES DE CRIMINALÍSTICA: 1 Conceitos básicos em Criminalística. 1.1 Inter-relação entre os Conceitos de Ciências Forenses. 1.2 Perícia criminal e civil. 1.3 Vestígio, Evidência e Indício. 1.4 Teoria dos vestígios. 1.5 Classificação dos vestígios quanto a sua natureza. 1.5.1 Vestígios Biológicos 1.5.2 Vestígios Físicos 1.5.3 Vestígios Químicos 1.5.4 Vestígios Morfológicos 1.5.5 Microvestígios. 1.6 Relação dos vestígios com os fatos e com o autor. 1.7 Fotografia Pericial. 1.7.1 Legislação aplicada. 1.7.2 Princípios e técnicas. 2 Noções sobre as principais áreas da Criminalística Moderna. 3 Locais de crime. 3.1 Definição de Local de crime. 3.2 O local como fonte de informação. 3.3 Isolamento e preservação de locais de crime. 3.4 Processamento pericial de locais de crime 3.4.1 Busca de vestígios. 3.4.2 Documentação do local. 3.4.3 Coleta de vestígios. 3.4.4 Acondicionamento. 3.4.5 Liberação do local. 3.5 Locais de crime contra a vida. 3.5.1 O exame perinecriscópico. 3.5.2 Tanatologia forense. 3.5.2.1 Sinais de morte. 3.5.3 Traumatologia Forense. 4 Balística Forense. 4.1 Conceito de arma de fogo. 4.2 Calibre. 4.3 Identificação. 4.4 O cartucho. 4.5 Resíduos do tiro. 4.6 Efeitos do tiro. 5 Princípios e elementos de um Laudo Pericial. 5.1 Objetivos principais. 6 Avanços e perspectivas de futuro em Ciências Forenses. 6.1 Rastreabilidade. 6.2 Análise de isótopos. 6.3 Banco de dados em Criminalística. 6.3.1 Banco de Perfis Genéticos 6.3.2 Banco de Perfis Balísticos.
DIREITOS HUMANOS: 1 Direitos humanos na Constituição Federal de 1988. 2 Sistema internacional de proteção dos direitos humanos. 3 Convenção para a Prevenção do Genocídio. 4 Convenção Relativa aos Refugiados. 5 Convenção sobre a Eliminação da Discriminação Racial. 6 Convenção da Mulher. 7 Convenção contra a Tortura. 8 Convenção Desaparecimento Forçado. 9 Regras mínimas da ONU (Presos). 10 Uso da Força. 11 Lei nº 13.060. 12. Decreto nº 12.341.
RACIOCÍNIO LÓGICO: 1 Estruturas lógicas. 2 Lógica de argumentação. 3 Lógica sentencial (ou proposicional). 3.1 Proposições simples e compostas. 3.2 Tabelas verdade. 3.3 Equivalências. 3.4 Leis de Morgan. 3.5 Diagramas lógicos. 4 Lógica de primeira ordem. 5 Princípios de contagem e probabilidade. 6 Operações com conjuntos. 7 Raciocínio lógico envolvendo problemas aritméticos, geométricos e matriciais."""

def parse_topics(text, edital_title, prefix=""):
    topics = []
    matches = list(re.finditer(r'(\d+(?:\.\d+)*)\s+', text))
    
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        chunk = text[start:end].strip()
        
        chunk = re.sub(r'\s+', ' ', chunk) # remove newlines
        chunk = chunk.rstrip('.')
        if len(chunk) > 3:
            name = f"{prefix}{chunk}" if prefix else chunk
            topics.append({"name": name, "tags": ["#edital"]})
            
    return {"title": edital_title, "topics": topics}

def seed_db():
    db = SessionLocal()
    
    edital_c4 = db.query(Edital).filter(Edital.title == "Perito Criminal Federal - Informática Forense").first()
    if edital_c4:
        db.delete(edital_c4)
    
    edital_cb = db.query(Edital).filter(Edital.title == "Conhecimentos Básicos - Perito Criminal Federal").first()
    if edital_cb:
        db.delete(edital_cb)
        
    db.commit()

    c4_data = parse_topics(text_cargo_4, "Perito Criminal Federal - Informática Forense")
    
    cb_topics = []
    for line in text_basico.split("\n"):
        if ":" in line:
            parts = line.split(":", 1)
            disciplina = parts[0].strip()
            content = parts[1].strip()
            parsed = parse_topics(content, "", prefix=f"{disciplina} - ")
            cb_topics.extend(parsed["topics"])
            
    cb_data = {"title": "Conhecimentos Básicos - Perito Criminal Federal", "topics": cb_topics}
    
    for data in [c4_data, cb_data]:
        edital = Edital(title=data["title"])
        db.add(edital)
        for t_obj in data["topics"]:
            topic = Topic(name=t_obj["name"][:250])
            for tag_name in t_obj.get("tags", []):
                tag_name = tag_name.lower().strip()
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name[:100])
                    db.add(tag)
                    db.flush()
                topic.tags.append(tag)
            edital.topics.append(topic)
            db.add(topic)
            
    db.commit()
    print("MUITO BEM SUCESSO ABSOLUTO")

if __name__ == "__main__":
    seed_db()
