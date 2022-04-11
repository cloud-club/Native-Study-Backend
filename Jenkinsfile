pipeline {
  agent any
  environment {
      UBUNTU_VERSOIN = "${env.UBUNTU_VERSION}"
      BUILD_VERSION = "${env.BUILD_VERSION}"
  }
  stages {
    stage('git scm update') {
      steps {
        git url: 'git@github.com:cloud-club/Native-Study-Backend.git', branch: 'develop'
      }
    }
    stage('docker build and push') {
      steps {
        sh '''
        docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml build --parallel

        docker tag music_service 192.168.56.10:8443/music_service

        docker tag mongo:5 192.168.56.10:8443/mongo

        docker tag quay.io/minio/mini:RELEASE.2022-04-09T15-09-52Z \
        192.168.56.10:8443/file_server

        docker push 192.168.56.10:8443/music_service \
        192.168.56.10:8443/file_server \
        192.168.56.10:8443/mongo
        '''
      }
    }
    stage('deploy kubernetes') {
      steps {
        sh '''
        kubectl apply -f backend-networkpolicy.yaml,file-server-deployment.yaml,\
        file-server-service.yaml,file-storage-persistentvolumeclaim.yaml,\
        mongo-deployment.yaml,mongo-persistentvolumeclaim.yaml,\
        mongo-service.yaml,music-service-deployment.yaml,\
        music-service-service.yaml

        kubectl expose deployment music_service_${BUILD_VERSION} \
        --type=LoadBalancer --port=8080 \
        --target-port=80 --name=music_service_svc
        '''
      }
    }
  }
}
