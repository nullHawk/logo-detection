for dir in test train valid; do
  for file in pepsi/$dir/labels/*.txt; do
    sed -i 's/^0/1/' "$file"
  done
done
mkdir -p combined/{test,train,valid}/{images,labels}
for dir in test train valid; do
  cp coca-cola/$dir/images/* combined/$dir/images/
  cp coca-cola/$dir/labels/* combined/$dir/labels/
  cp pepsi/$dir/images/* combined/$dir/images/
  cp pepsi/$dir/labels/* combined/$dir/labels/
done
