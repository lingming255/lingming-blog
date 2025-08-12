---
date: '2025-08-08T13:33:18.617923'
draft: false
publish: true
title: 个人网站 (lingming.art) 持久化部署作战手册
---

# 个人网站 (lingming.art) 持久化部署作战手册

---

## 一、作战目标 (Objective)

在本地网络（局域网）的NAS设备上，通过Docker容器运行一个网站服务，并利用Cloudflare Tunnel技术，将其安全、稳定地发布到公共互联网，实现通过域名 `https://lingming.art` 的全球访问。本手册旨在固化部署流程，确保未来可快速、无差错地重建该系统。

## 二、核心组件清单 (Bill of Materials)

1.  **网站服务容器 (Website Service Container):**
    *   **角色:** 运行你的网站程序 (如Caddy, Hugo, Nginx等) 的Docker容器。
    *   **关键配置:** 必须将容器内部的Web端口（如`80`）映射到NAS的一个固定端口上。
    *   **本次战役配置:** 容器内部`80`端口 -> NAS`192.168.1.184`的`40915`端口。

2.  **Cloudflare Tunnel容器 (`cloudflared`):**
    *   **角色:** 部署在NAS上的“内应”，负责创建一条连接到Cloudflare全球网络的安全加密隧道。
    *   **关键配置:** 包含唯一身份令牌（Token）的Docker指令。
    *   **本次战役配置:** 使用`cloudflare/cloudflared`官方镜像。

3.  **Cloudflare云端服务:**
    *   **角色:** 提供DNS解析、隧道管理和安全防护的总指挥部。
    *   **关键配置:**
        *   **DNS记录:** 一条由隧道自动生成的`CNAME`记录。
        *   **隧道公共主机名:** 将公网域名指向NAS上暴露的本地服务地址。

## 三、作战流程 (Standard Operating Procedure)

### 步骤1：确保本地服务端口就绪 (Prerequisite: Local Service Port)

在执行任何公网发布操作前，必须确保你的网站服务在局域网内是可访问的。

1.  **检查网站容器的端口映射：** 确保你的网站容器启动时，包含了端口映射参数，例如 `-p 40915:80`。
2.  **本地回路验证：** 在局域网内的任何设备上，打开浏览器，访问 `http://192.168.1.184:40915`。必须能够正常看到你的网站页面。**此步骤不成功，切勿继续。**

### 步骤2：配置Cloudflare指挥部 (Cloudflare DNS & Tunnel Creation)

1.  登录Cloudflare仪表板，进入 `lingming.art` 域。
2.  **清理DNS战场 (极其重要):**
    *   前往左侧菜单 **DNS > Records (记录)**。
    *   **删除**任何现存的、名称为 `lingming.art` 或 `www` 的 `A`, `AAAA`, `CNAME` 记录。目的是为隧道自动生成的记录扫清障碍，避免冲突。
3.  **创建隧道并获取令牌:**
    *   前往左侧菜单 **Zero Trust**。
    *   在Zero Trust仪表板中，进入 **Access > Tunnels (访问 > 隧道)**。
    *   点击 **Create a tunnel (创建隧道)**。
    *   选择 `Cloudflared` 作为连接器，点击 **Next**。
    *   为隧道命名 (例如 `nas-website-tunnel`)，点击 **Save tunnel**。
    *   在 **"Install and run a connector"** 页面，选择 **Docker**。你会看到一条 `docker run ...` 指令，其中包含了你的**唯一身份令牌 (Token)**。复制并保存这条完整的指令。

### 步骤3：部署NAS前线节点 (Deploying the Tunnel on NAS)

1.  通过SSH登录到你的NAS (`192.168.1.184`)。
2.  执行以下**【最终版】**Docker指令，它包含了后台运行、自动重启等持久化参数。请将 `<你的隧道令牌>` 替换为你在上一步中获取的真实令牌。

    ```bash
    sudo docker run -d --restart unless-stopped --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <你的隧道令牌>
    ```

    **本次战役使用的精确指令备份：**
    ```bash
    sudo docker run -d --restart unless-stopped --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token eyJhIjoiYTlhYjNhM2UxZjBlNzQ2MDBjNDA2MDc1ZmY1YTA2M2MiLCJ0IjoiZDExNmEzMWYtNWY5MC00YmFjLTgxNzctZmI5MDE5ZDZiNGI1IiwicyI6Ik0yWTFNakkyWW1FdE9EUTRNaTAwTnpRM0xUZzFZemt0TWpGaE9XUXpabUV5TmpCaiJ9
    ```
3.  **验证部署状态:**
    *   执行 `sudo docker ps`，确认名为 `cloudflare-tunnel` 的容器处于 `Up` 状态。
    *   执行 `sudo docker logs cloudflare-tunnel`，确认日志中出现多条指向Cloudflare不同数据中心（如`sjc06`, `sjc08`）的 `Registered tunnel connection` 信息。

### 步骤4：配置公共路由 (Configuring the Public Hostname)

当NAS上的隧道容器成功运行后，返回Cloudflare的隧道配置页面。

1.  在你的隧道列表中，点击 **Configure (配置)**。
2.  选择 **Public Hostname (公共主机名)** 标签页。
3.  点击 **Add a public hostname (添加公共主机名)**。
4.  **填写路由信息:**
    *   **Hostname (主机名):** `lingming.art`
    *   **Service / Type (服务 / 类型):** `HTTP`
    *   **Service / URL (服务 / URL):** `192.168.1.184:40915`
5.  点击 **Save hostname (保存主机名)**。

完成此步骤后，Cloudflare会自动在你的DNS区域为你创建正确的`CNAME`记录。等待几分钟全球DNS同步后，即可通过 `https://lingming.art` 访问。

---

## 四、关键代码与配置清单 (Quick Reference)

*   **NAS局域网IP:** `192.168.1.184`
*   **网站容器端口映射:** `40915:80` (公网 -> 容器)
*   **隧道指向的本地URL:** `http://192.168.1.184:40915`
*   **Cloudflared持久化部署指令:** `sudo docker run -d --restart unless-stopped --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <你的隧道令牌>`
#待整理