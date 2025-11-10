//+------------------------------------------------------------------+
//|                                          TradingAI_DataExporter.mq5 |
//|                                  Expert Advisor para Trading AI    |
//|                        Exporta dados do MT5 para análise Python    |
//+------------------------------------------------------------------+
#property copyright "Trading AI"
#property link      ""
#property version   "1.00"
#property strict

//--- Parâmetros de entrada
input string   DataFolder = "TradingAI";           // Pasta para arquivos compartilhados
input string   Symbol_Name = "";                   // Símbolo (vazio = atual)
input ENUM_TIMEFRAMES Timeframe = PERIOD_M5;      // Timeframe
input int      NumCandles = 15;                    // Número de candles para análise
input int      UpdateInterval = 60;                // Intervalo de atualização (segundos)
input bool     ShowSignals = true;                 // Mostrar setas no gráfico
input bool     EnableAlerts = true;                // Ativar alertas sonoros

//--- Variáveis globais
datetime lastUpdate = 0;
string symbol;
string dataPath;
string signalPath;

//+------------------------------------------------------------------+
//| Função de inicialização do Expert                                |
//+------------------------------------------------------------------+
int OnInit()
{
   //--- Define símbolo
   if(Symbol_Name == "")
      symbol = _Symbol;
   else
      symbol = Symbol_Name;

   //--- Cria pasta de dados se não existir
   string terminalPath = TerminalInfoString(TERMINAL_DATA_PATH);
   string folderPath = terminalPath + "\\MQL5\\Files\\" + DataFolder;

   //--- Paths dos arquivos
   dataPath = DataFolder + "\\candles_data.csv";
   signalPath = DataFolder + "\\signals.csv";

   //--- Mensagem de inicialização
   Print("==============================================");
   Print("Trading AI Expert Advisor Iniciado");
   Print("==============================================");
   Print("Símbolo: ", symbol);
   Print("Timeframe: ", EnumToString(Timeframe));
   Print("Candles: ", NumCandles);
   Print("Pasta de dados: ", folderPath);
   Print("==============================================");

   //--- Exportar dados iniciais
   ExportCandlesData();

   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Função principal (executada a cada tick)                         |
//+------------------------------------------------------------------+
void OnTick()
{
   //--- Verificar intervalo de atualização
   datetime currentTime = TimeCurrent();

   if(currentTime - lastUpdate >= UpdateInterval)
   {
      //--- Exportar dados dos candles
      ExportCandlesData();

      //--- Ler sinais do Python
      ReadSignals();

      //--- Atualizar timestamp
      lastUpdate = currentTime;
   }
}

//+------------------------------------------------------------------+
//| Exporta dados dos candles para CSV                               |
//+------------------------------------------------------------------+
void ExportCandlesData()
{
   //--- Obter dados dos candles
   MqlRates rates[];
   ArraySetAsSeries(rates, true);

   int copied = CopyRates(symbol, Timeframe, 0, NumCandles + 50, rates);

   if(copied <= 0)
   {
      Print("Erro ao copiar dados dos candles: ", GetLastError());
      return;
   }

   //--- Abrir arquivo para escrita
   int fileHandle = FileOpen(dataPath, FILE_WRITE|FILE_CSV|FILE_ANSI, ",");

   if(fileHandle == INVALID_HANDLE)
   {
      Print("Erro ao criar arquivo: ", GetLastError());
      return;
   }

   //--- Escrever cabeçalho
   FileWrite(fileHandle, "time", "open", "high", "low", "close", "tick_volume", "real_volume", "spread");

   //--- Escrever dados
   for(int i = 0; i < copied; i++)
   {
      FileWrite(fileHandle,
                TimeToString(rates[i].time, TIME_DATE|TIME_MINUTES),
                DoubleToString(rates[i].open, _Digits),
                DoubleToString(rates[i].high, _Digits),
                DoubleToString(rates[i].low, _Digits),
                DoubleToString(rates[i].close, _Digits),
                IntegerToString(rates[i].tick_volume),
                IntegerToString(rates[i].real_volume),
                IntegerToString(rates[i].spread)
               );
   }

   //--- Fechar arquivo
   FileClose(fileHandle);

   Print("Dados exportados: ", copied, " candles");
}

//+------------------------------------------------------------------+
//| Lê sinais do arquivo Python                                      |
//+------------------------------------------------------------------+
void ReadSignals()
{
   //--- Verificar se arquivo existe
   if(!FileIsExist(signalPath))
   {
      //Print("Arquivo de sinais não encontrado (Python ainda não processou)");
      return;
   }

   //--- Abrir arquivo para leitura
   int fileHandle = FileOpen(signalPath, FILE_READ|FILE_CSV|FILE_ANSI, ",");

   if(fileHandle == INVALID_HANDLE)
   {
      Print("Erro ao abrir arquivo de sinais: ", GetLastError());
      return;
   }

   //--- Ler cabeçalho
   string header = FileReadString(fileHandle);

   //--- Ler última linha (sinal mais recente)
   string lastLine = "";
   while(!FileIsEnding(fileHandle))
   {
      lastLine = FileReadString(fileHandle);
   }

   //--- Fechar arquivo
   FileClose(fileHandle);

   //--- Processar sinal
   if(lastLine != "")
   {
      ProcessSignal(lastLine);
   }
}

//+------------------------------------------------------------------+
//| Processa o sinal recebido                                        |
//+------------------------------------------------------------------+
void ProcessSignal(string signalLine)
{
   string parts[];
   int count = StringSplit(signalLine, ',', parts);

   if(count < 5)
      return;

   //--- Parsear dados do sinal
   // Formato: timestamp,signal,confidence,strategy,reason
   string timestamp = parts[0];
   int signal = (int)StringToInteger(parts[1]);
   double confidence = StringToDouble(parts[2]);
   string strategy = parts[3];
   string reason = parts[4];

   //--- Mostrar sinal no gráfico
   if(ShowSignals)
   {
      DisplaySignalOnChart(signal, confidence, strategy, reason);
   }

   //--- Alerta sonoro
   if(EnableAlerts && signal != 0)
   {
      string alertMsg = "";

      if(signal == 1)
         alertMsg = "🟢 COMPRA: " + strategy + " (" + DoubleToString(confidence*100, 1) + "%)";
      else if(signal == -1)
         alertMsg = "🔴 VENDA: " + strategy + " (" + DoubleToString(confidence*100, 1) + "%)";

      if(alertMsg != "")
      {
         Alert(alertMsg);
         Print(alertMsg);
         Print("Razão: ", reason);
      }
   }
}

//+------------------------------------------------------------------+
//| Exibe sinal no gráfico                                           |
//+------------------------------------------------------------------+
void DisplaySignalOnChart(int signal, double confidence, string strategy, string reason)
{
   if(signal == 0)
      return;

   //--- Nome único para o objeto
   string objName = "TradingAI_Signal_" + TimeToString(TimeCurrent());

   //--- Obter último preço
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   CopyRates(symbol, Timeframe, 0, 1, rates);

   if(ArraySize(rates) == 0)
      return;

   double price = rates[0].close;
   datetime time = rates[0].time;

   //--- Criar seta
   if(signal == 1) // Compra
   {
      ObjectCreate(0, objName, OBJ_ARROW_BUY, 0, time, price);
      ObjectSetInteger(0, objName, OBJPROP_COLOR, clrLime);
      ObjectSetInteger(0, objName, OBJPROP_WIDTH, 3);
   }
   else if(signal == -1) // Venda
   {
      ObjectCreate(0, objName, OBJ_ARROW_SELL, 0, time, price);
      ObjectSetInteger(0, objName, OBJPROP_COLOR, clrRed);
      ObjectSetInteger(0, objName, OBJPROP_WIDTH, 3);
   }

   //--- Criar texto com informações
   string textName = objName + "_Text";
   string text = strategy + "\n" + DoubleToString(confidence*100, 1) + "%";

   ObjectCreate(0, textName, OBJ_TEXT, 0, time, price);
   ObjectSetString(0, textName, OBJPROP_TEXT, text);
   ObjectSetInteger(0, textName, OBJPROP_COLOR, signal == 1 ? clrLime : clrRed);
   ObjectSetInteger(0, textName, OBJPROP_FONTSIZE, 8);

   //--- Atualizar gráfico
   ChartRedraw();
}

//+------------------------------------------------------------------+
//| Função de finalização do Expert                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("Trading AI Expert Advisor Finalizado");
}

//+------------------------------------------------------------------+
//| Função de tratamento de comentários no gráfico                   |
//+------------------------------------------------------------------+
void OnTimer()
{
   //--- Atualizar status no canto do gráfico
   string status = "Trading AI - Ativo\n";
   status += "Última atualização: " + TimeToString(lastUpdate, TIME_DATE|TIME_MINUTES) + "\n";
   status += "Símbolo: " + symbol + "\n";
   status += "Aguardando sinais do Python...";

   Comment(status);
}
