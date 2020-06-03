<p align="center"><img width=50% src="https://github.com/TBFY/general/blob/master/figures/tbfy-logo.png"></p>
<p align="center"><img width=40% src="https://github.com/TBFY/platform/blob/master/logo.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v3+-blue.svg)
![Docker-Compose](https://img.shields.io/badge/docker_compose-v3.0+-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/TBFY/platform.svg)](https://github.com/TBFY/platform/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Basic Overview

Easy deployment of TheyBuyForYou tools and services into a local environment.

## Quick Start

This process has been tested in an environment with 4 CPUs and 4GB RAM

1. Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
1. Clone this repo

	```
	git clone https://github.com/TBFY/platform.git
	```
1. Download the latest TBFY data dump from Zenodo into a temporal folder (e.g  `/tmp`).
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3712322.svg)](https://doi.org/10.5281/zenodo.3712322)
1. Run the platform by:
    ```
    docker-compose up -d
    ```
1. Wait for all services to be available (e.g. `Started Application in xx.xx seconds`). The first time it may take a few minutes to download the Docker images.
    ```
    docker-compose logs -f
	```
1. Initialize the RDF repository
    1. Log into the Fuseki administration GUI, [http://localhost:3030](http://localhost:3030), using the `admin` user and the password that you set in the `fuseki.env` file.
    1. Create a new dataset `tbfy` with the dataset type `Persistent (TDB2)`.
    1. Upload the NACE and OpenCorporates identifer system data files from [here](https://github.com/TBFY/knowledge-graph/tree/master/data).
    1. Follow [these instructions](https://github.com/TBFY/knowledge-graph/tree/master/python-scripts) to publish the TBFY procurement data. First set the environment variable `TBFY_FUSEKI_URL` to:     
       ```
        export TBFY_FUSEKI_URL=http://localhost:3030
	   ```
1. Initialize the Document repository
    1. Unzip the `TBFY_DATA_DUMP_JSON.zip` file from the temporal folder. The content is organized by month in different folders.    
        ```
        unzip /tmp/TBFY_DATA_DUMP_JSON.zip 
	   ```
    1. Load the tender descriptions using the `index_tenders.py` python script. Depending on the number of folders selected (e.g `/tmp/*` or `/tmp/2020-04-*` or `/tmp/2020-04-30`), the operation may take minutes or hours.:
        ```
        ./script/index_tenders.py -i /tmp/2020-04-30
	   ```
1. That's all! 

## Services

Once the platform is up and running, all TBFY services are available from a single entry point:

|               service                                                   |            description                             |
|-------------------------------------------------------------------------|----------------------------------------------------|
|    [/industryCodes](http://localhost:8000/industryCodes)                |    industry codes                                  |
|    [/jurisdictions](http://localhost:8000/jurisdictions)                |    jurisdictions                                   |
|    [/ocds](http://localhost:8000/ocds)          	                      |    OCDS instances                                  |
|    [/brands](http://localhost:8000/brands)                              |    organization names                              |
|    [/triples](http://localhost:8000/triples)                            |    SPARQL Endpoint                                 |
|    [/documents](http://localhost:8000/documents)                        |    tender descriptions                             |
|    [/organisation](http://localhost:8000/organisation)                  |    organizations                                   |
|    [/contract](http://localhost:8000/contract)                          |    contracts                                       |
|    [/tender](http://localhost:8000/tender)                              |    tenders                                         |
|    [/award](http://localhost:8000/award)                                |    awards                                          |
|    [/contractingProcess](http://localhost:8000/contractingProcess)      |    contracting processes                           |

## Resources

TBFY services are supported by the following resources:

|               resource                                                    |          description                   |
|---------------------------------------------------------------------------|----------------------------------------|
|    [http://localhost:8085](http://localhost:8085)                         | English Topic Model      	             |
|    [http://localhost:8086](http://localhost:8086)                         | Spanish Topic Model      	             |          
|    [http://localhost:8087](http://localhost:8087)                         | French Topic Model      	             |         
|    [http://localhost:8088](http://localhost:8088)                         | Italian Topic Model      	             |
|    [http://localhost:8089](http://localhost:8089)                         | Portuguese Topic Model      	         |        
|    [http://localhost:8983](http://localhost:8083)                         | Document Repository                    |  
|    [http://localhost:8983/solr/banana](http://localhost:8983/solr/banana) | Dashboard                              |
|    [http://localhost:3040](http://localhost:3040)                         | SPARQL Query Interface                 |
|    [http://localhost:3030](http://localhost:3030)                         | RDF Repository                         |


## Contributing
Please take a look at our [contributing](https://github.com/TBFY/general/blob/master/guides/how-to-contribute.md) guidelines if you're interested in helping!
