#!/bin/bash
gitlabToken=LGvfX6XFT9fQuSisxY5g
gitlabURL="https://git.voziq.com"
projectApi="/api/v4/projects"
userApi="/api/v4/users"
groupApi="/api/v4/groups"
namespacesAPI="/api/v4/namespaces"
gitlabProjTemplate="https://git.voziq.com/root/models-project-template.git"
defaultNamespace="ailab"
ProjectLocalBasePath="$1"
projectName="$2"
projectUserName="$3"

#Verify If Project Exists in GitLab
isGitlabProjectExist(){
        existStatus=""
        responseCode=""
        responseLength=""
        apiRequest=$(curl -k --write-out "%{http_code};%{size_download}" --silent --connect-timeout 10 --no-keepalive --output /dev/null \
                                        -XGET --header "PRIVATE-TOKEN: $gitlabToken" $gitlabURL/$projectApi?search="$1")
        IFS=';' read -a apiResponse <<< "${apiRequest}"
        responseCode=${apiResponse[0]}
        responseLength=${apiResponse[1]}
        if ([ $responseCode -eq 200 ] && [ $responseLength -gt 2 ]); then
                existStatus=1
        else
                existStatus=0
        fi
        echo $existStatus
}

#Verify If Project Directory Exist in Local Storage
isProjectDirExist(){
        basePath="$1"
        projectName="$2"
        existStatus=""
        if [ -d "$ProjectLocalBasePath" ]; then
                existStatus=1
        else
                existStatus=0
        fi
        echo $existStatus
}


#Get User Attributes From GitLab
gitlabAPIGetProjectAttributes(){
        gitlabPrjId=""
        apiResponseUserId=
        apiRequest=$(curl -k --write-out "%{http_code};%{size_download}" --silent --connect-timeout 10 --no-keepalive \
                                        -XGET --header "PRIVATE-TOKEN: $gitlabToken" $gitlabURL/$projectApi?search="$1")
        # gitlabUserId=$(echo $apiRequest | grep -o -E "\"id\":[0-9]+" | awk -F\: '{print $2}')
	    gitlabPrjId=$(echo $apiRequest | grep -Po '"name":.*?[^\\]"' | awk -F\: '{print $2}' | tr -d '""')			  
        echo $gitlabPrjId
}

#Create GitLab Project For User
gitlabAPIDeleteProject(){
        gitlabProjectName=$1
        ProjectLocalBasePath=$2
        gitlabPrjId=$(gitlabAPIGetProjectAttributes "$1")                
	    arr=("$gitlabPrjId") 					
		for i in ${arr[*]}
            do       			
        if [ "$i" = "$gitlabProjectName" ]; then   
echo "Strings are  equal $i  and $gitlabProjectName"       
	        gitlabPrjIds=""
	        apiRequest=$(curl -k --write-out "%{http_code};%{size_download}" --silent --connect-timeout 10 --no-keepalive \
                                        -XGET --header "PRIVATE-TOKEN: $gitlabToken" $gitlabURL/$projectApi?search="$i")
            gitlabPrjIds=$(echo $apiRequest | grep -o -E "\"id\":[0-9]+" | awk -F\: '{print $2}')
        
        fi
            done	 				
                prjId=`echo $gitlabPrjIds | cut -d" " -f1`
                nameapceId=`echo $gitlabPrjIds | cut -d" " -f2`
                echo $prjId
                echo $nameapceId

                existStatus=""
             if [[ $(isGitlabProjectExist "$gitlabProjectName") -eq 1 ]] || [[ $(isProjectDirExist "$gitlabProjectName") -eq 1 ]] && [[ ! -z "$prjId" ]]; then
		    apiRequest=$(curl -k --write-out "%{http_code};%{size_download}" --silent --connect-timeout 10 --no-keepalive \
                                        -XDELETE --header "PRIVATE-TOKEN: $gitlabToken" $gitlabURL//$projectApi/$prjId)
										rm -rf $ProjectLocalBasePath
                         existStatus=0
                
                    else
                  existStatus=1
			    	exit 9       
                  fi
                echo $existStatus
}
gitlabAPIDeleteProject "$projectName" "$ProjectLocalBasePath" "$projectUserName" "$defaultNamespace"