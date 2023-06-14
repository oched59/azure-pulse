# DATA.AI-Azure-OpenAI-Microsoft-Advisor-Bot

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=599293758&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json&location=WestUs2)
[![Open in Remote - Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/AMBGASG/DATA.AI-Azure-OpenAI-Microsoft-Advisor-Bot)

This project is about creating a PoC for a chat bot which advises on Microsoft updates & technology.
The bot is based on Power Platform at the frontend and uses Azure & OpenAI ChatGPT in the background to generate text.

## Architecture

![Architecture Overview](docs/architecture/Application%20Blueprint.png)

## Features

* Chat interface
* APIs to interact with knowledge backend

## Getting Started

> **IMPORTANT:** In order to deploy and run this demo, you'll need an **Azure subscription with access enabled for the Azure OpenAI service**. You can request access [here](https://aka.ms/oaiapply). You can also visit [here](https://azure.microsoft.com/free/cognitive-search/) to get some free Azure credits to get you started.

> **AZURE RESOURCE COSTS** by default this demo will create Azure resources that have monthly costs and costs per use.

### Prerequisites

#### To Run Locally
Provided setup is Windows based. Change tools for setup within Linux or MacOS.
- [Powershell 7+ (pwsh)](https://github.com/powershell/powershell)
   - **Important**: Ensure you can run `pwsh.exe` from a PowerShell command. If this fails, you likely need to upgrade PowerShell.
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Git](https://git-scm.com/downloads)
- [Git WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git)
- [VSCode](https://code.visualstudio.com/download)
- [VSCode DevContainer](https://code.visualstudio.com/docs/devcontainers/containers#_system-requirements)
  - **Important**: Recommended open source alternative to Docker
  - [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation/)
  - [Rancher Desktop VSCode Remote](https://docs.rancherdesktop.io/how-to-guides/vs-code-remote-containers/)

>NOTE: Your Azure Account must have [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner) permissions. You must be an [Power Platform Administrator](https://learn.microsoft.com/en-us/power-platform/admin/use-service-admin-role-manage-tenant#power-platform-administrator) within Power Platform to create the required resources.

#### To Run in GitHub Codespaces or VS Code Remote Containers

You can run this repo virtually by using GitHub Codespaces or VS Code Remote Containers.  Click on one of the buttons below to open this repo in one of those options.

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=brightgreen&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=599293758&machine=standardLinux32gb&devcontainer_path=.devcontainer%2Fdevcontainer.json&location=WestUs2)
[![Open in Remote - Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/AMBGASG/DATA.AI-Azure-OpenAI-Microsoft-Advisor-Bot)

### Project Initialization

* TBD on how to initialize the project

### Quickstart

* TBD on how to quickly use the solution

## Resources

* [Sample solution - ChatGPT + Enterprise data with Azure OpenAI and Cognitive Search](https://github.com/Azure-Samples/azure-search-openai-demo)
* [Azure OpenAI samples](https://github.com/Azure/azure-openai-samples)
* [Revolutionize your Enterprise Data with ChatGPT: Next-gen Apps w/ Azure OpenAI and Cognitive Search](https://aka.ms/entgptsearchblog)
* [Azure Cognitive Search](https://learn.microsoft.com/azure/search/search-what-is-azure-search)
* [Azure OpenAI Service](https://learn.microsoft.com/azure/cognitive-services/openai/overview)

### FAQ

***Question***: A common question ABC

***Answer***: Answer to common question

### Troubleshooting

* TBD No troubleshooting steps know yet