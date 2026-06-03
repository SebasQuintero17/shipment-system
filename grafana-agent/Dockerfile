FROM grafana/agent:latest

COPY agent.yml /etc/agent/agent.yml

ENTRYPOINT ["/bin/grafana-agent"]
CMD ["-config.file=/etc/agent/agent.yml"]
