<div align="center"><a name="readme-top"></a>

# daily high light

this is a open source flask project that can use ai to create a daily highlight of your day.

</div>

<details>
<summary><kbd>Table of contents</kbd></summary>

#### TOC

- [daily high light](#daily-high-light)
      - [TOC](#toc)
      - [](#)
  - [Before Setup](#before-setup)
  - [Quick Start](#quick-start)
  - [Features View](#features-view)

####

<br/>

</details>

## Before Setup

this project require ollama to run, make sure you have it installed before running the project.

[![][ollama-icon]][ollama-download-link]

> \[!IMPORTANT]
>
> make sure your ollama is running at port 11343, else this project will not work.

## Quick Start

1. Clone the repository  
``` bash
git clone https://github.com/PhalisZequlard/daily-high-light.git
```
2. download [ollama][ollama-download-link]
3. in ollama, pull a model
``` bash
ollama pull qwen2.5-coder:0.5b
```
4. change the model to yours in the code
5. run flask

## Features View
- intelligent summary
- local storage
- easy to use
<details><summary><h4>🖥️ Demo video</h4></summary>

<div align="center"><a name="readme-top"></a>

![][demo-gif]

</details>

---

<details><summary><h4>📝 License</h4></summary>

This project is licensed under the Apache 2.0 License

</details>

Copyright © 2024 [Zequlard][profile-link]. <br />
This project is Apache 2.0 licensed.

<!-- LINK GROUP -->


[profile-link]: https://github.com/PhalisZequlard/daily-high-light  
[ollama-icon]: media/icon/ollama-icon-rounded.png
[ollama-download-link]: https://ollama.com/download
[demo-gif]: media/demo/daily-high-light-demo.gif