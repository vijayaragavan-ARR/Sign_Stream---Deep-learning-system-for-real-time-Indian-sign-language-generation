using UnrealBuildTool;

public class SignStreamServerTarget : TargetRules
{
	public SignStreamServerTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Server;
		ExtraModuleNames.Add("SignStream");
	}
}
