using UnrealBuildTool;

public class SignStreamTarget : TargetRules
{
	public SignStreamTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Game;
		ExtraModuleNames.Add("SignStream");
	}
}
