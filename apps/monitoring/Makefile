# Monitoring Makefile
.PHONY: up down build restart logs clean status health

# Include the common Makefile
include ../Makefile.common

test:
	@echo "Checking otel-collector metrics endpoint..."
	@curl -sf http://localhost:8889/metrics > /dev/null \
	    && echo "otel-collector is healthy!" \
	    || (echo "otel-collector is NOT healthy!" && exit 1)