#!/bin/bash

echo "This script will set the following environment variables: AZURE_SUBSCRIPTION_ID, AZURE_TENANT, AZURE_CLIENT_ID, AZURE_SECRET"
echo "SECURITY WARNING: This script will append the environment variables to the end of the .bashrc file in the home directory."
echo "Use this script only if you are sure you want to set these environment variables."
echo "Do you want to continue? (y/n)"
read CONTINUE


echo "Enter the value for AZURE_SUBSCRIPTION_ID:"
read AZURE_SUBSCRIPTION_ID

echo "Enter the value for AZURE_TENANT:"
read AZURE_TENANT

echo "Enter the value for AZURE_CLIENT_ID:"
read AZURE_CLIENT_ID

echo "Enter the value for AZURE_SECRET:"
read -s AZURE_SECRET

echo "export AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID" >> ~/.bashrc
echo "export AZURE_TENANT=$AZURE_TENANT" >> ~/.bashrc
echo "export AZURE_CLIENT_ID=$AZURE_CLIENT_ID" >> ~/.bashrc
echo "export AZURE_SECRET=$AZURE_SECRET" >> ~/.bashrc

echo "Environment variables set and added to .bashrc!"
