🌱 EcoTrack
Sprint 2 — Protótipo Funcional

FIAP | Disruptive Architectures: IoT, IoB & Generative IA

🧭 Visão Geral

O EcoTrack é um projeto voltado à criação de um sistema IoT que monitora variáveis ambientais em tempo real, simulando sensores que enviam dados via protocolo MQTT.
Nesta sprint, o foco foi desenvolver um protótipo funcional usando Node-RED e o broker HiveMQ, com tentativa de integração ao Oracle APEX.

👥 Integrantes
RM	Nome
RM560685	Gustavo Dantas
RM560262	Paulo Neto
RM559906	Davi Vasconcelos Souza

🚀 Objetivos da Sprint 2
Criar um fluxo funcional no Node-RED

Simular dispositivos IoT enviando dados via MQTT

Testar o uso do broker HiveMQ

Iniciar integração com o Oracle APEX

Planejar uso futuro de IA Generativa para análise dos dados

⚙️ Protótipo Desenvolvido

O protótipo simula sensores que publicam dados de temperatura, umidade e nível de CO₂.
Esses dados são publicados no tópico ecotrack/sensor01 e recebidos pelo próprio Node-RED através do broker HiveMQ.

Exemplo de Payload recebido:
{
  "deviceId": "sensor01",
  "temperature": "21.4",
  "humidity": "57.8",
  "co2": "0.37",
  "timestamp": "2025-11-10T01:16:40.434Z"
}


💡 Isso confirma que o broker MQTT está recebendo e retransmitindo as mensagens corretamente.

🧩 Código do Nó “Gerar Dados Simulados”
msg.payload = {
    deviceId: "sensor01",
    temperature: (20 + Math.random() * 5).toFixed(1),
    humidity: (50 + Math.random() * 10).toFixed(1),
    co2: (0.3 + Math.random() * 0.2).toFixed(2),
    timestamp: new Date().toISOString()
};
return msg;
🔹 Este código gera valores aleatórios que simulam leituras de um sensor IoT.
🔹 A cada execução, ele envia uma nova leitura formatada em JSON para o broker MQTT.

🧠 Fluxo Node-RED (Descrição)
Gerar Dados Simulados (Function): cria o payload IoT.

Publicar no MQTT: envia para o tópico ecotrack/sensor01.

Debug / Payload Recebido: exibe no console os dados publicados.

(Opcional) HTTP Request: tentativa de envio ao Oracle APEX.

🧰 Tecnologias Utilizadas
Categoria	Ferramenta	Descrição
IoT	Node-RED	Criação do fluxo e automação de mensagens
Comunicação	HiveMQ (Broker MQTT)	Intermedia a troca de mensagens entre dispositivos simulados
Cloud / Backend	Oracle APEX	Tentativa de integração via API REST
IA / ML	Planejado	Uso futuro de IA generativa para análise dos dados

🧩 Desafios e Aprendizados
Dificuldade inicial na autenticação com o Oracle APEX

Compreensão do funcionamento dos brokers MQTT e tópicos

Uso prático do Node-RED para integrações IoT

Entendimento da comunicação publish/subscribe

🧱 Próximos Passos
Finalizar a integração com Oracle APEX

Criar tabela para armazenar dados MQTT

Implementar API REST para envio automático

Aplicar IA generativa ou analítica simples (ex: detecção de anomalias)

Melhorar o dashboard e visualização dos dados

🔗 Links Importantes

🧠 Broker MQTT (HiveMQ): https://www.hivemq.com/demos/websocket-client/
💾 Repositório GitHub: [link aqui]
🎥 Vídeo da Apresentação: https://youtu.be/yT3fGPyvLxQ

🏁 Conclusão
Mesmo sem a integração completa ao Oracle APEX, o EcoTrack demonstra com sucesso o envio e recebimento de dados IoT via MQTT, consolidando o aprendizado sobre Node-RED, brokers MQTT e comunicação entre dispositivos.
Este protótipo serve como base sólida para as próximas sprints, nas quais serão aplicadas soluções de IA e armazenamento em nuvem.
