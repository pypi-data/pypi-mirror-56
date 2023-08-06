<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/banner.svg?sanitize=true" alt="Nboost" width="70%">
</p>

<p align="center">
<a href="https://cloud.drone.io/koursaros-ai/nboost">
    <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />
</a>
<a href="https://pypi.org/project/nboost/">
    <img src="https://img.shields.io/pypi/pyversions/nboost.svg" />
</a>
<a href="https://pypi.org/project/nboost/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/nboost.svg">
</a>
<a href='https://nboost.readthedocs.io/en/latest/'>
    <img src='https://readthedocs.org/projects/nboost/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://www.codacy.com/app/koursaros-ai/nboost?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=koursaros-ai/nboost&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/a9ce545b9f3846ba954bcd449e090984"/>
</a>
<a href="https://codecov.io/gh/koursaros-ai/neural_rerank">
  <img src="https://codecov.io/gh/koursaros-ai/neural_rerank/branch/master/graph/badge.svg" />
</a>
<a href='https://github.com/koursaros-ai/nboost/blob/master/LICENSE'>
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/nboost.svg">
</a>
</p>

<p align="center">
  <a href="#highlights">Highlights</a> •
  <a href="#overview">Overview</a> •
  <a href="#install-nboost">Install</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="https://nboost.readthedocs.io/">Documentation</a> •
  <a href="#tutorial">Tutorial</a> •
  <a href="#contributing">Contributing</a> •
  <a href="./CHANGELOG.md">Release Notes</a> •
  <a href="https://koursaros-ai.github.io/Live-Fact-Checking-Algorithms-in-the-Era-of-Fake-News/">Blog</a>  
</p>

<h2 align="center">What is it</h2>

⚡**NBoost** is a scalable, search-engine-boosting platform for developing and deploying state-of-the-art models to improve the relevance of search results.

<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/overview.svg?sanitize=true" width="100%">
</p>

Nboost leverages finetuned models to produce domain-specific neural search engines. The platform can also improve other downstream tasks requiring ranked input, such as question answering.

<a href = '#contact'>Contact us to request domain-specific models or leave feedback</a>

<h2 align="center">Overview</h2>
<center>

Fine-tuned Models                       | Domain              | Search Boost<sup>[4]</sup> | Speed
--------------------------------------- | ------------------- | -------------------------- | -------------
`bert-base-uncased-msmarco`(**default**)<a href='#footnotes'><sup>[1]</sup></a>| <a href ='http://www.msmarco.org/'>bing queries</a> | **0.302** vs 0.173 (1.8x)  | 301 ms/query<a href='#footnotes'><sup>[3]</sup></a>
`biobert-base-uncased-pubmed` <i>(coming soon)</i>| <a href ='http://bioasq.org/'>medicine</a>  | - | -
`bert-tiny-uncased` <i>(coming soon)</i>| -  | - | -
`albert-tiny-uncased-msmarco` <i>(coming soon)</i>| -  | - | ~50ms/query <a href='#footnotes'><sup>[3]</sup></a>

</center>

These cutting edge models have as much as **doubled** search relevance. While assessing performance, there is often a tradeoff between model accuracy and speed, so we benchmark both of these factors above. This leaderboard is a work in progress, and we intend on releasing more cutting edge models!

<sup>[4]</sup> <a href = 'https://en.wikipedia.org/wiki/Mean_reciprocal_rank'>Mean Reciprocal Rank </a> compared to BM25, the default for Elasticsearch. Reranking top 100.

<h2 align="center">Install NBoost</h2>

There are two ways to get NBoost, either as a Docker image or as a PyPi package. **For cloud users, we highly recommend using NBoost via Docker**. 
> 🚸 Depending on your model, you should install the respective Tensorflow or Pytorch dependencies. We package them below.

For installing NBoost, follow the table below.
<center>

Dependency      | 🐳 Docker                             | 📦 Pypi                     | 🚦Status
--------------- | ------------------------------------- | --------------------------  | -------------
**-**        | `koursaros/nboost:latest-alpine`      | `pip install nboost`        | <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />
**Pytorch**     | `koursaros/nboost:latest-torch`       | `pip install nboost[torch]` | <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />
**Tensorflow**  | `koursaros/nboost:latest-tf`          | `pip install nboost[tf]`    | <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />
**All**         | `koursaros/nboost:latest-all`         | `pip install nboost[all]`   | <img src="https://cloud.drone.io/api/badges/koursaros-ai/nboost/status.svg" />

</center>

Any way you install it, if you end up reading the following message after `$ nboost --help` or `$ docker run koursaros/nboost --help`, then you are ready to go!

<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/cli-help.svg?sanitize=true" alt="success installation of NBoost">
</p>


<h2 align="center">Getting Started</h2>

- [The Proxy](#the-proxy)
- [Setting up a Neural Proxy for Elasticsearch in 3 minutes](#Setting-up-a-Neural-Proxy-for-Elasticsearch-in-3-minutes)
  * [Setting up an Elasticsearch Server](#setting-up-an-elasticsearch-server)
  * [Deploying the proxy](#deploying-the-proxy)
  * [Indexing some data](#indexing-some-data)
- [Elastic made easy](#elastic-made-easy)
- [Deploying a distributed proxy via Docker Swarm/Kubernetes](#deploying-a-proxy-via-docker-swarmkubernetes)
- [‍Take-home messages](#take-home-messages)


### 📡The Proxy

<center>
<table>
  <tr>
  <td width="33%">
      <img src="https://github.com/koursaros-ai/nboost/raw/master/.github/rocket.svg?sanitize=true" alt="component overview">
      </td>
  <td>
  <p>The <a href="http://nboost.readthedocs.io/en/latest/chapter/proxy.html">Proxy</a> is the core of NBoost. The proxy is essentially a wrapper to enable serving the model. It is able to understand incoming messages from specific search apis (i.e. Elasticsearch). When the proxy receives a message, it increases the amount of results the client is asking for so that the model can rerank a larger set and return the (hopefully) better results.</p>
  <p>For instance, if a client asks for 10 results to do with the query "brown dogs" from Elasticsearch, then the proxy may increase the results request to 100 and filter down the best ten results for the client.</p>
</td>
  </tr>
</table>
</center>

#### 



### Setting up a Neural Proxy for Elasticsearch in 3 minutes

In this example we will set up a proxy to sit in between the client and Elasticsearch and boost the results!

#### Setting up an Elasticsearch Server
> 🔔 If you already have an Elasticsearch server, you can move on to the next step!

If you don't have Elasticsearch, not to worry! You can set up a local Elasticsearch cluster by using docker. First, get the ES image by running:
```bash
docker pull elasticsearch:7.4.2
```
Once you have the image, you can run an Elasticsearch server via:
```bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.4.2
```

#### Deploying the proxy
Now we're ready to deploy our Neural Proxy! It is very simple to do this, simply run:
```bash
nboost --uhost localhost --uport 9200 --field passage
```
> 📢 The `--uhost` and `--uport` should be the same as the Elasticsearch server above! Uhost and uport are short for upstream-host and upstream-port (referring to the upstream server).

If you get this message: `Listening: <host>:<port>`, then we're good to go!

#### Indexing some data
The proxy is set up so that there is no need to ever talk to the server directly from here on out. You can send index requests, stats requests, but only the search requests will be altered. For demonstration purposes, we will be indexing [a set of passages about open-source software](https://microsoft.github.io/TREC-2019-Deep-Learning/) through NBoost. You can add the index to your Elasticsearch server by running:
```bash
nboost-tutorial Travel --host localhost --port 8000
```` 

Now let's test it out! Go to your web browser and type in:
```bash
curl "http://localhost:8000/travel/_search?pretty&q=passage:vegas&size=2"
```

If the Elasticsearch result has the `_nboost` tag in it, congratulations it's working!

What just happened? You asked for two results from Elasticsearch having to do with "vegas". The proxy intercepted this request, asked the Elasticsearch for 10 results, and the model picked the best two. Magic! 🔮 (statistics)

<p align="center">
<img src="https://github.com/koursaros-ai/nboost/raw/master/.github/cli-help.svg?sanitize=true" alt="success installation of NBoost">
</p>

#### Elastic made easy
To increase the number of parallel proxies, simply increase `--workers`. For a more robust deployment approach, you can distribute the proxy [via Docker Swarm or Kubernetes](#Deploying-a-proxy-via-Docker-Swarm/Kubernetes).

### Deploying a proxy via Docker Swarm/Kubernetes
> 🚧 Swarm yaml/Helm chart under construction...


<h2 align="center">Documentation</h2>

[![ReadTheDoc](https://readthedocs.org/projects/nboost/badge/?version=latest&style=for-the-badge)](https://nboost.readthedocs.io)

The official NBoost documentation is hosted on [nboost.readthedocs.io](http://nboost.readthedocs.io/). It is automatically built, updated and archived on every new release.

<h2 align="center">Tutorial</h2>

> 🚧 Under construction.

<h2 align="center">Benchmark</h2>

We have setup `/benchmarks` to track the network/model latency over different NBoost versions.


<h2 align="center">Contributing</h2>

Contributions are greatly appreciated! You can make corrections or updates and commit them to NBoost. Here are the steps:

1. Create a new branch, say `fix-nboost-typo-1`
2. Fix/improve the codebase
3. Commit the changes. Note the **commit message must follow [the naming style](./CONTRIBUTING.md#commit-message-naming)**, say `Fix/model-bert: improve the readability and move sections`
4. Make a pull request. Note the **pull request must follow [the naming style](./CONTRIBUTING.md#commit-message-naming)**. It can simply be one of your commit messages, just copy paste it, e.g. `Fix/model-bert: improve the readability and move sections`
5. Submit your pull request and wait for all checks passed (usually 10 minutes)
    - Coding style
    - Commit and PR styles check
    - All unit tests
6. Request reviews from one of the developers from our core team.
7. Merge!

More details can be found in the [contributor guidelines](./CONTRIBUTING.md).

<h2 align="center">Citing NBoost</h2>

If you use NBoost in an academic paper, we would love to be cited. Here are the two ways of citing NBoost:

1.     \footnote{https://github.com/koursaros-ai/nboost}
2. 
    ```latex
    @misc{koursaros2019NBoost,
      title={NBoost: Neural Boosting Search Results},
      author={Thienes, Cole and Pertschuk, Jack},
      howpublished={\url{https://github.com/koursaros-ai/nboost}},
      year={2019}
    }
    ```

<h2 align="center">Footnotes</h2>

<sup>[1]</sup> https://github.com/nyu-dl/dl4marco-bert <br/>
<sup>[2]</sup> https://github.com/huggingface/transformers <br/>
<sup>[3]</sup> ms for reranking each hit. On nvidia T4 GPU. <br/>

<h2 align="center">License</h2>

If you have downloaded a copy of the NBoost binary or source code, please note that the NBoost binary and source code are both licensed under the [Apache License, Version 2.0](./LICENSE).

<sub>
Koursaros AI is excited to bring this open source software to the community.<br>
Copyright (C) 2019. All rights reserved.
</sub>