#  Dockerfile to build the cammisboto3 container
FROM docker.io/library/amazonlinux:latest as installer
RUN echo "proxy=http://10.151.204.100:8080" >> /etc/yum.conf
# Things that might change (version numbers, etc.) or reused
ENV BIN_DIR "/usr/local/bin"
ENV KUBECTL_VERSION "1.26.1"
ENV HELM_VERSION "v3.11.1"
ENV ARGO_Version "v2.0.3"
ENV TARGETOS "linux"
ENV TARGETARCH "amd64"
ENV KUSTOMIZE_VERSION "5.0.0"
RUN yum update -y \
  && yum install -y unzip \
  && yum install -y zip \
  && yum install -y wget \
  && yum install -y openssl \
  && yum install -y tar \
  && yum install -y jq \
  && yum install -y python3 python3-pip \
  && python3 -m pip install boto3 pandas s3fs terminaltables progressbar2\
  && curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip \
  && unzip -o -q awscliv2.zip \
  # The --bin-dir is specified so that we can copy the
  # entire bin directory from the installer stage into
  # into /usr/local/bin of the final stage without
  # accidentally copying over any other executables that
  # may be present in /usr/local/bin of the installer stage.
  && ./aws/install --bin-dir /aws-cli-bin \
  # Install git
  && yum install -y git \
  && git init \
  # Install kubectl
  && wget https://storage.googleapis.com/kubernetes-release/release/v1.26.1/bin/linux/amd64/kubectl \
  && chmod +x kubectl \
  && mv kubectl ${BIN_DIR} \
 # install kustomize 
  && curl -fL https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v${KUSTOMIZE_VERSION}/kustomize_v${KUSTOMIZE_VERSION}_${TARGETOS}_${TARGETARCH}.tar.gz | tar xz \                                 
  && chmod +x kustomize \
  && mv kustomize ${BIN_DIR} \   
 # Install Helm
  && curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
  && chmod 700 get_helm.sh \
  && ./get_helm.sh
RUN unset http_proxy
RUN unset https_proxy
FROM docker.io/library/amazonlinux:latest
RUN echo "proxy=http://10.151.204.100:8080" >> /etc/yum.conf
COPY --from=installer /usr/ /usr/
COPY --from=installer /aws-cli-bin/ /usr/local/bin/
RUN yum update -y \
  && yum install -y less groff \
  && yum clean all
RUN unset http_proxy
RUN unset https_proxy
ENTRYPOINT ["/bin/sh"]
