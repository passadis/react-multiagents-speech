<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=azure,react,nodejs,py,docker,vscode" />
  </a>
</p>

<h1 align="center">React and Azure Text to Speech with Container Apps</h1>

## Introduction

This project is about building a React Web App with a Python Backend, hosting 3 different Speech Agents. The Web App offers different use cases of Azure Speech services particularly Azure Text to Speech with Python calling external APIs and making our Application "speak" the results, on weather, news or stock exchange. Everything is hosted on Azure Container Apps with Azure Container Registry supporting our Docker Images.
## Architecture of Our Workshop

Our workshop showcases an architecture involving:

- A **Python Flask Web App** as the frontend.
- A **Python-based container image** as the backend API endpoint.

The frontend allows users to select a city from a drop-down menu and receive information and photos of that city. The backend service fetches photographs stored in a Storage Account and uses the OpenAI Chat Completions API to retrieve general information about the selected city. This setup can be extended into a full-fledged tourist or travel web application, complete with security, scalability, redundancy, and flexibility.

## Building the Application

We'll use Azure CLI for a straightforward approach to building our resources:


This approach offers an integrated solution for enterprise-scale applications, ready for production with features like Azure Redis Cache for enhanced performance.

## Contribute

We encourage contributions! If you have ideas on how to improve this application or want to report a bug, please feel free to open an issue or submit a pull request.

## Architecture
