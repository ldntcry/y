python3 -m compileall .
if [ $? -ne 0 ]; then
  exit 1
fi

BOT_COMMAND="python3 -m usu"
RESTART_DELAY=5

while true; do
  echo "$(date): Starting bot..."
  ${BOT_COMMAND}
  RETVAL=$?
  if [ $RETVAL -eq 0 ] || [ $RETVAL -eq 137 ]; then
    echo "$(date): Bot stopped manually. Not restarting."
    break
  else
    echo "$(date): Bot stopped with error $RETVAL. Restarting in ${RESTART_DELAY} seconds..."
    sleep ${RESTART_DELAY}
  fi
done
