import 'package:flutter_test/flutter_test.dart';
import 'package:omb_companion/main.dart';

void main() {
  testWidgets('OpenMotorBridge companion app smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const OmbCompanionApp());
    expect(find.text('OpenMotorBridge'), findsOneWidget);
  });
}
