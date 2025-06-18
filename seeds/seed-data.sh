#!/bin/bash

seeds_path="seeds/"

# First confirmation
read -r -p "⚠️  WARNING: This will reset your database data. Do you want to continue? (y/N): " confirm1
if [[ "$confirm1" != "y" && "$confirm1" != "Y" ]]; then
  echo "❌ Operation aborted."
  exit 1
fi

# Second confirmation
read -r -p "⚠️  Type 'SEED-DATABASE-WITH-INITIAL-VALUE' to confirm: " confirm2
if [[ "$confirm2" != "SEED-DATABASE-WITH-INITIAL-VALUE" ]]; then
  echo "❌ Operation aborted."
  exit 1
fi

# Proceed with loading fixtures
fixtures=$(ls $seeds_path)
while IFS= read -r fixture; do
   if [[ $fixture == *.json ]]; then
     echo -n "Seeding "
     echo $fixture
     python3 manage.py loaddata "$seeds_path/$fixture"
   fi
done <<< "$fixtures"
