typeset model_db="model.db"
typeset site_db="site.db"
typeset destination="../dentalhcrm"
typeset backup="./backup"
typeset timestamp=$(date +%Y%m%d_%H%M%S)

if [[ -f $destination/$site_db ]]; then
   cp $destination/$site_db $backup/$site_db.$timestamp
fi
cp $model_db $destination/$site_db
