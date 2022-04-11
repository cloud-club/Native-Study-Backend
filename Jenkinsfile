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
        docker build --build-arg UBUNTU_VERSION=${UBUNTU_VERSION} \
        -t 192.168.56.10:8443/music_service:${BUILD_VERSION} .
        docker push 192.168.56.10:8443/${BUILD_VERSION}
        '''
      }
    }
    stage('deploy kubernetes') {
      steps {
        sh '''
        kubectl create deployment music_service_${BUILD_VERSION} --image=192.168.56.10:8443/music_service:${BUILD_VERSION}
        kubectl expose deployment music_service_${BUILD_VERSION} --type=LoadBalancer --port=8080 \
                                               --target-port=80 --name=music_service_svc
        '''
      }
    }
  }
}
