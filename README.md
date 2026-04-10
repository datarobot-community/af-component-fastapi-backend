<p align="center">
  <a href="https://github.com/datarobot-community/af-component-fastapi-backend">
    <img src="https://af.datarobot.com/img/datarobot_logo.avif" width="600px" alt="DataRobot Logo"/>
  </a>
</p>
<p align="center">
    <span style="font-size: 1.5em; font-weight: bold; display: block;">af-component-fastapi-backend</span>
</p>

<p align="center">
  <a href="https://datarobot.com">Homepage</a>
  ·
  <a href="https://af.datarobot.com">Documentation</a>
  ·
  <a href="https://docs.datarobot.com/en/docs/get-started/troubleshooting/general-help.html">Support</a>
</p>

<p align="center">
  <a href="https://github.com/datarobot-community/af-component-fastapi-backend/tags">
    <img src="https://img.shields.io/github/v/tag/datarobot-community/af-component-fastapi-backend?label=version" alt="Latest Release">
  </a>
  <a href="/LICENSE">
    <img src="https://img.shields.io/github/license/datarobot-community/af-component-fastapi-backend" alt="License">
  </a>
</p>

The FastAPI Component. Deploys a DataRobot Custom Application with a FastAPI server

This component provides the structure for a FastAPI backend that can be deployed as a DataRobot Custom Application. It's designed for app developers building App Framework templates that need a Python API layer, and it integrates cleanly with the [React frontend component](https://github.com/datarobot-community/af-component-react). The component is part of the [App Framework Studio](https://af.datarobot.com) ecosystem.

The repo ships a FastAPI application scaffold and the configuration needed to deploy it as a DataRobot Custom Application. Because the component is repeatable, a single template can include multiple independent FastAPI backends — apply this component more than once, each with a distinct `fastapi_app` name.

# Table of contents

- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
- [Component dependencies](#component-dependencies)
  - [Required](#required)
  - [Local development](#local-development)
  - [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Next steps and cross-links](#next-steps-and-cross-links)
- [Contributing, changelog, support, and legal](#contributing-changelog-support-and-legal)

# Prerequisites

Before applying this component, ensure your environment meets the following requirements.

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) installed
- [`dr`](https://cli.datarobot.com) installed
- A DataRobot account with permissions to create Custom Applications.
- The [`af-component-base`](https://github.com/datarobot-community/af-component-base) component must already be applied to your project (see [Component dependencies](#component-dependencies)).

# Quick start

Run the following command in your project directory:

```bash
dr component add https://github.com/datarobot-community/af-component-fastapi-backend .
```

If you need additional control, you can run this to use copier directly:

```bash
uvx copier copy datarobot-community/af-component-fastapi-backend .
```

During the copy, the wizard asks for a `fastapi_app` name. Use a short, lowercase identifier (for example, `api` or `backend`). If your template needs multiple FastAPI backends, apply this component again with a different name — the component is repeatable.

After applying, verify the server starts by running `uv run uvicorn FASTAPI_APP.app:app --reload --port 8080` and hitting `http://localhost:8080/health`.

# Component dependencies

This component requires the `base` component to be applied first. The sections below list required dependencies, local development setup, and how to keep the component up to date.

## Required

The following components must be applied to the project **before** this component:

| Name | Repository | Repeatable |
|------|-----------|------------|
| `base` | [https://github.com/datarobot-community/af-component-base](https://github.com/datarobot-community/af-component-base) | No |

## Local development

Run the FastAPI server locally with `uv`:

```bash
uv run uvicorn FASTAPI_APP.app:app --reload --port 8080
```

The server is available at `http://localhost:8080`. Use the `/health` endpoint as a quick smoke test:

```bash
curl http://localhost:8080/health
```

**Key paths:**

| Path | Purpose |
|------|---------|
| `FASTAPI_APP/app.py` | FastAPI application entrypoint. |
| `FASTAPI_APP/routes/` | Route definitions. |
| `pyproject.toml` | Project dependencies and metadata. |

When working in a Codespace, forward port `8080` to access the server from your browser.

## Updating

All components should be regularly updated to pick up bug fixes, new features, and compatibility with the latest DataRobot App Framework.

For automatic updates to the latest version, run the following command in your project directory:

```bash
dr component update .datarobot/answers/fastapi-FASTAPI_APP_NAME.yml
```

If you need more fine-grained control and prefer using copier directly, you can run this to have more control over the process:

```bash
uvx copier update -a .datarobot/answers/fastapi-FASTAPI_APP_NAME.yml -A
```

# Troubleshooting

Common setup and runtime issues are listed below by symptom.

**`uvx copier copy` fails with a merge conflict**
Ensure `af-component-base` is applied first. This component expects base scaffolding to be present before it runs.

**`uv run` reports a missing package**
Run `uv sync` to install dependencies declared in `pyproject.toml`.

**Application fails to start on DataRobot**
Check the Custom Application logs in the DataRobot UI. The most common cause is a missing environment variable — confirm all required runtime parameters are set in the deployment configuration.

**Port conflict on local dev**
Change the `--port` flag in the `uvicorn` command, or stop any other process already bound to port `8080`.

# Next steps and cross-links

Use these resources to go deeper with the component and the broader App Framework ecosystem.

- [App Framework documentation](https://af.datarobot.com)&mdash;full component catalog, architecture overview, and deployment guides.
- [af-component-react](https://github.com/datarobot-community/af-component-react)&mdash;pair this backend with a React frontend.
- [af-component-base](https://github.com/datarobot-community/af-component-base)&mdash;required base component.
- [DataRobot Custom Applications docs](https://docs.datarobot.com/en/docs/wb-apps/custom-apps/upload-custom-app.html)&mdash;runtime parameters, app hosting, and environment configuration.

# Contributing, changelog, support, and legal

- **Contributing**&mdash;fork the repository, create a feature branch, and open a pull request. Run `task lint` before submitting. See `CONTRIBUTING.md` for the full process.
- **Changelog**&mdash;see `CHANGELOG.md` for version history. This project follows semantic versioning.
- **Getting help**&mdash;open a [GitHub Issue](https://github.com/datarobot-community/af-component-fastapi-backend/issues) for bugs or feature requests. For general DataRobot support, visit the [support portal](https://docs.datarobot.com/en/docs/get-started/troubleshooting/general-help.html).
- **License**&mdash;Apache 2.0 — see [LICENSE](/LICENSE).
