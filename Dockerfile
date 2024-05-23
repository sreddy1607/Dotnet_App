
#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM registry.access.redhat.com/ubi8/dotnet-60-runtime AS base
WORKDIR /app
RUN chown 1001:1001 -R .


FROM registry.access.redhat.com/ubi8/dotnet-60 AS build
USER root
WORKDIR /src

RUN chown 1001:1001 -R .
COPY ["provider-portal-detec-service.csproj", ""]
RUN dotnet nuget add source https://nexusrepo-tools.apps.bld.cammis.medi-cal.ca.gov/repository/nuget.org-proxy/index.json -n nuget.org-proxy -u Jenkins-builder -p  --store-password-in-clear-text
RUN dotnet nuget setapikey 7eb5424c-5f47-381c-b1fa-8c8592508455 -source https://nexusrepo-tools.apps.bld.cammis.medi-cal.ca.gov/repository/cammis-dotnet-repo-group/
RUN dotnet restore "./provider-portal-detec-service.csproj"
COPY . .
WORKDIR "/src/."
RUN mkdir -p /app/build
RUN mkdir -p /app/publish
RUN chown 1001:1001 -R /app/build
RUN chown 1001:1001 -R /app/publish
RUN chmod -vR 777 /app/build
RUN chmod -vR 777 /app/publish
RUN dotnet build "provider-portal-detec-service.csproj" -c Release -o /app/build

#FROM build AS publish
RUN dotnet publish "provider-portal-detec-service.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
USER 1001
WORKDIR /app
#COPY --from=publish /app/publish .
COPY  --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:9007
EXPOSE 9007
ENTRYPOINT ["dotnet", "provider-portal-detec-service.dll"]
